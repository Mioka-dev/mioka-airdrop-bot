import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from translations import get_translation
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

# تنظیمات Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توکن ربات از متغیرهای محیطی Render
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# URL وب سرویس شما در Render
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PORT = int(os.environ.get('PORT', 8080))

ADMIN_USERNAME = 'MiokaToken'
AIRDROP_LIMIT = 4000
AIRDROP_TOKEN_AMOUNT = 10000
DIRECT_REFERRAL_BONUS = 6000
INDIRECT_REFERRAL_BONUS = 4000

# لینک‌ها و مأموریت‌ها
LINKS = {
    'telegram_channel': 'https://t.me/MiokaTokenofficial',
    'twitter_page': 'https://x.com/miokatoken',
    'retweet_link': 'https://x.com/miokatoken/status/1926174873056874644?t=5Fdz6a9wNPVKPaj7pcrh7w&s=19',
    'website': 'https://miokatoken.org'
}

# یک دیکشنری ساده برای ذخیره اطلاعات کاربران.
users_data = {}
referred_by = {}
completed_airdrop_users = set()

def get_user_state(user_id):
    return users_data.get(user_id, {}).get('state', 'start')

def set_user_state(user_id, state):
    if user_id not in users_data:
        users_data[user_id] = {}
    users_data[user_id]['state'] = state

def get_user_language(user_id):
    return users_data.get(user_id, {}).get('lang', 'en')

def set_user_language(user_id, lang):
    if user_id not in users_data:
        users_data[user_id] = {}
    users_data[user_id]['lang'] = lang

def get_referral_link(user_id, bot_username):
    return f"https://t.me/{bot_username}?start={user_id}"

def get_referral_counts(user_id):
    direct_count = sum(1 for uid, referrer_id in referred_by.items() if referrer_id == user_id)
    indirect_count = sum(1 for uid, referrer_id in referred_by.items() if referrer_id in [ruid for ruid, rrid in referred_by.items() if rrid == user_id])
    return direct_count, indirect_count

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    referrer_id = None
    if context.args and context.args[0].isdigit():
        referrer_id = int(context.args[0])
        if user_id != referrer_id and user_id not in referred_by and len(completed_airdrop_users) < AIRDROP_LIMIT:
            referred_by[user_id] = referrer_id

    if user_id in completed_airdrop_users:
        lang = get_user_language(user_id)
        bot_username = (await context.bot.get_me()).username
        link = get_referral_link(user_id, bot_username)
        direct_count, indirect_count = get_referral_counts(user_id)
        total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
        
        text = get_translation(lang, "already_joined_message")
        
        keyboard = [
            [InlineKeyboardButton(get_translation(lang, "my_tokens_button"), callback_data='my_tokens')],
            [InlineKeyboardButton(get_translation(lang, "my_referral_link_button"), callback_data='my_referral_link')],
            [InlineKeyboardButton(get_translation(lang, "my_referrals_button"), callback_data='my_referrals')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if len(completed_airdrop_users) >= AIRDROP_LIMIT:
        await update.message.reply_text(get_translation('en', "airdrop_finished"))
        return

    set_user_state(user_id, 'choose_lang')
    keyboard = [
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')],
        [InlineKeyboardButton("日本語 🇯🇵", callback_data='lang_jp')],
        [InlineKeyboardButton("Français 🇫🇷", callback_data='lang_fr')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose your language:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_language(user_id)
    await query.answer()

    if query.data.startswith('lang_'):
        lang = query.data.split('_')[1]
        set_user_language(user_id, lang)
        set_user_state(user_id, 'welcoming')
        
        welcome_text = get_translation(lang, "welcome_message")
        keyboard = [[InlineKeyboardButton(get_translation(lang, "join_telegram_button"), url=LINKS['telegram_channel'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=welcome_text, reply_markup=reply_markup, parse_mode='HTML')
        await query.message.reply_text(get_translation(lang, "after_join_telegram_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_translation(lang, "done_button"), callback_data='done_telegram')]]))

    elif query.data == 'done_telegram':
        set_user_state(user_id, 'ask_telegram_username')
        await query.edit_message_text(get_translation(lang, "enter_telegram_username"))

    elif query.data == 'done_twitter_retweet':
        set_user_state(user_id, 'ask_twitter_username')
        await query.edit_message_text(get_translation(lang, "enter_twitter_username"))

    elif query.data == 'done_website':
        set_user_state(user_id, 'ask_wallet_address')
        await query.edit_message_text(get_translation(lang, "enter_wallet_address"))

    elif query.data == 'my_tokens':
        direct_count, indirect_count = get_referral_counts(user_id)
        total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
        await query.edit_message_text(get_translation(lang, "my_tokens_message").format(total_tokens=f"{total_tokens:,}"))

    elif query.data == 'my_referral_link':
        bot_username = (await context.bot.get_me()).username
        link = get_referral_link(user_id, bot_username)
        await query.edit_message_text(get_translation(lang, "your_referral_link_message").format(referral_link=link))

    elif query.data == 'my_referrals':
        direct_count, indirect_count = get_referral_counts(user_id)
        await query.edit_message_text(get_translation(lang, "your_referrals_message").format(direct=direct_count, indirect=indirect_count))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = update.message.text
    lang = get_user_language(user_id)
    state = get_user_state(user_id)
    
    if update.effective_user.username == ADMIN_USERNAME and text == "/admin":
        await send_admin_data(update, context)
        return

    if state == 'ask_telegram_username':
        users_data[user_id]['telegram_username'] = text
        set_user_state(user_id, 'ask_twitter_follow')
        
        keyboard = [[InlineKeyboardButton(get_translation(lang, "follow_twitter_button"), url=LINKS['twitter_page'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_translation(lang, "after_telegram_username_message"), reply_markup=reply_markup)
        await update.message.reply_text(get_translation(lang, "after_follow_twitter_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_translation(lang, "retweet_button"), url=LINKS['retweet_link'])]]))
        await update.message.reply_text(get_translation(lang, "after_retweet_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_translation(lang, "done_button"), callback_data='done_twitter_retweet')]]))

    elif state == 'ask_twitter_username':
        users_data[user_id]['twitter_username'] = text
        set_user_state(user_id, 'ask_website_visit')
        
        keyboard = [[InlineKeyboardButton(get_translation(lang, "visit_website_button"), url=LINKS['website'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_translation(lang, "after_twitter_username_message"), reply_markup=reply_markup)
        await update.message.reply_text(get_translation(lang, "after_visit_website_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_translation(lang, "done_button"), callback_data='done_website')]]))

    elif state == 'ask_wallet_address':
        users_data[user_id]['wallet_address'] = text
        set_user_state(user_id, 'completed')
        completed_airdrop_users.add(user_id)

        direct_count, indirect_count = get_referral_counts(user_id)
        total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
        
        thank_you_text = get_translation(lang, "thank_you_message")
        
        keyboard = [
            [InlineKeyboardButton(get_translation(lang, "my_tokens_button"), callback_data='my_tokens')],
            [InlineKeyboardButton(get_translation(lang, "my_referral_link_button"), callback_data='my_referral_link')],
            [InlineKeyboardButton(get_translation(lang, "my_referrals_button"), callback_data='my_referrals')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(thank_you_text, reply_markup=reply_markup)

    else:
        pass

async def send_admin_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.username == ADMIN_USERNAME:
        try:
            import pandas as pd
            
            data_list = []
            for user_id, user_info in users_data.items():
                if 'wallet_address' in user_info:
                    direct_count, indirect_count = get_referral_counts(user_id)
                    total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
                    
                    data_list.append({
                        'Telegram ID': user_id,
                        'Telegram Username': user_info.get('telegram_username', 'N/A'),
                        'Twitter Username': user_info.get('twitter_username', 'N/A'),
                        'Wallet Address': user_info.get('wallet_address', 'N/A'),
                        'Referred By ID': referred_by.get(user_id, 'N/A'),
                        'Direct Referrals': direct_count,
                        'Indirect Referrals': indirect_count,
                        'Total Tokens': total_tokens,
                    })
            
            df = pd.DataFrame(data_list)
            file_path = "participants.xlsx"
            df.to_excel(file_path, index=False)
            
            await update.message.reply_document(open(file_path, 'rb'))
            os.remove(file_path)
        except ImportError:
            await update.message.reply_text("Please install 'pandas' and 'openpyxl' to generate the Excel file.")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # This is a very basic way to handle updates, not recommended for production
            # but works for simple deployments
            update = Update.de_json(json.loads(post_data.decode('utf-8')), application.bot)
            
            # Asynchronous processing of the update
            threading.Thread(target=asyncio.run, args=(application.process_update(update),)).start()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            logging.error(f"Error processing webhook update: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error")

async def start_webhook_server():
    # Setup the application
    global application
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run the application in webhook mode
    await application.bot.setWebhook(url=WEBHOOK_URL)
    await application.run_webhook(listen="0.0.0.0", port=PORT, webhook_url=WEBHOOK_URL)

    # Start the simple HTTP server
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, WebhookHandler)
    logging.info(f"Starting httpd on port {PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set!")
        exit(1)
    if not WEBHOOK_URL:
        logging.error("WEBHOOK_URL is not set!")
        exit(1)
    
    asyncio.run(start_webhook_server())