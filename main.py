import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import asyncio
import io
import csv

# Logging Settings
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Bot Token from Render Environment Variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PORT = int(os.environ.get('PORT', 8080))

# Your Admin Telegram ID
ADMIN_ID = 7578618644
AIRDROP_LIMIT = 4000
AIRDROP_TOKEN_AMOUNT = 10000
DIRECT_REFERRAL_BONUS = 6000
INDIRECT_REFERRAL_BONUS = 4000

# Mission Links
LINKS = {
    'telegram_channel': 'https://t.me/MiokaTokenofficial',
    'twitter_page': 'https://x.com/miokatoken',
    'retweet_link': 'https://x.com/miokatoken/status/1926174873056874644?t=5Fdz6a9wNPVKPaj7pcrh7w&s=19',
    'website': 'https://miokatoken.org'
}

# In-memory storage for users. This will be wiped on restart.
users_data = {}
referred_by = {}
completed_airdrop_users = set()

# Simplified texts (for this version, all in English to avoid translation issues)
TEXTS = {
    "welcome_message": "Welcome to Mioka Airdrop!\nComplete all missions to earn <b>10,000</b> $MIOKA tokens.\n\nHere are the first steps:",
    "join_telegram_button": "Join Telegram Channel",
    "after_join_telegram_message": "Perfect! Now that you've joined our channel, tap the 'Done' button.",
    "done_button": "Done",
    "enter_telegram_username": "Please send me your Telegram username (e.g., @MiokaToken).",
    "after_telegram_username_message": "Great! Now let's move to the Twitter mission.",
    "follow_twitter_button": "Follow on Twitter",
    "after_follow_twitter_message": "Thank you! Please tap 'Done' after following our Twitter page.",
    "retweet_button": "Retweet Pinned Post",
    "after_retweet_message": "Tap 'Done' after retweeting our pinned post.",
    "enter_twitter_username": "Please send me your Twitter username (e.g., @MiokaToken).",
    "after_twitter_username_message": "Awesome! Now let's visit our website.",
    "visit_website_button": "Visit Website",
    "after_visit_website_message": "Tap 'Done' after visiting our website.",
    "enter_wallet_address": "Finally, please send me your BSC Wallet address.",
    "thank_you_message": "Thank you! You have successfully joined the airdrop. Your tokens will be distributed after the airdrop ends.",
    "my_tokens_button": "My Tokens",
    "my_referral_link_button": "My Referral Link",
    "my_referrals_button": "My Referrals",
    "my_tokens_message": "You have earned <b>{total_tokens:,}</b> $MIOKA tokens.",
    "your_referral_link_message": "Your personal referral link:\n<code>{referral_link}</code>\n\nShare this link to earn <b>6,000</b> $MIOKA for each direct referral and <b>4,000</b> $MIOKA for each indirect referral.",
    "your_referrals_message": "You have <b>{direct}</b> direct referrals and <b>{indirect}</b> indirect referrals.",
    "already_joined_message": "You have already joined the airdrop.",
    "airdrop_finished": "The airdrop has reached its limit and is now closed."
}

def get_text(key):
    return TEXTS.get(key, "Error: Text not found.")

def get_user_state(user_id):
    return users_data.get(user_id, {}).get('state', 'start')

def set_user_state(user_id, state):
    if user_id not in users_data:
        users_data[user_id] = {}
    users_data[user_id]['state'] = state

def get_referral_link(user_id, bot_username):
    return f"https://t.me/{bot_username}?start={user_id}"

def get_referral_counts(user_id):
    direct_count = sum(1 for uid, referrer_id in referred_by.items() if referrer_id == user_id)
    indirect_count = sum(1 for uid, referrer_id in referred_by.items() if referrer_id in [ruid for ruid, rrid in referred_by.items() if rrid == user_id])
    return direct_count, indirect_count

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id if user_id == ADMIN_ID:
        await admin_command(update, context)
        return

    referrer_id = None
    if context.args and context.args[0].isdigit():
        referrer_id = int(context.args[0])
        if user_id != referrer_id and user_id not in referred_by and len(completed_airdrop_users) < AIRDROP_LIMIT:
            referred_by[user_id] = referrer_id

    if user_id in completed_airdrop_users:
        text = get_text("already_joined_message")
        
        keyboard = [
            [InlineKeyboardButton(get_text("my_tokens_button"), callback_data='my_tokens')],
            [InlineKeyboardButton(get_text("my_referral_link_button"), callback_data='my_referral_link')],
            [InlineKeyboardButton(get_text("my_referrals_button"), callback_data='my_referrals')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)
        return

    if len(completed_airdrop_users) >= AIRDROP_LIMIT:
        await update.message.reply_text(get_text("airdrop_finished"))
        return

    set_user_state(user_id, 'telegram_mission_step_1')
    
    welcome_text = get_text("welcome_message")
    keyboard = [[InlineKeyboardButton(get_text("join_telegram_button"), url=LINKS['telegram_channel'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode='HTML')
    
    await context.bot.send_message(chat_id=user_id, text=get_text("after_join_telegram_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text("done_button"), callback_data='done_telegram')]]))

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id == ADMIN_ID:
        keyboard = [[InlineKeyboardButton("Get Airdrop Data", callback_data='get_admin_data')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Admin Panel:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if user_id == ADMIN_ID and query.data != 'get_admin_data':
        return
        
    if query.data == 'done_telegram':
        set_user_state(user_id, 'ask_telegram_username')
        await query.edit_message_text(get_text("enter_telegram_username"))

    elif query.data == 'done_twitter_follow':
        set_user_state(user_id, 'twitter_mission_step_2')
        keyboard = [[InlineKeyboardButton(get_text("retweet_button"), url=LINKS['retweet_link'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(get_text("after_follow_twitter_message"), reply_markup=reply_markup)
        await context.bot.send_message(chat_id=user_id, text=get_text("after_retweet_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text("done_button"), callback_data='done_twitter_retweet')]]))

    elif query.data == 'done_twitter_retweet':
        set_user_state(user_id, 'ask_twitter_username')
        await query.edit_message_text(get_text("enter_twitter_username"))

    elif query.data == 'done_website':
        set_user_state(user_id, 'ask_wallet_address')
        await query.edit_message_text(get_text("enter_wallet_address"))
    
    elif query.data == 'my_tokens':
        direct_count, indirect_count = get_referral_counts(user_id)
        total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
        await context.bot.send_message(chat_id=user_id, text=get_text("my_tokens_message").format(total_tokens=f"{total_tokens:,}"))

    elif query.data == 'my_referral_link':
        bot_username = (await context.bot.get_me()).username
        link = get_referral_link(user_id, bot_username)
        await context.bot.send_message(chat_id=user_id, text=get_text("your_referral_link_message").format(referral_link=link))

    elif query.data == 'my_referrals':
        direct_count, indirect_count = get_referral_counts(user_id)
        await context.bot.send_message(chat_id=user_id, text=get_text("your_referrals_message").format(direct=direct_count, indirect=indirect_count))

    elif query.data == 'get_admin_data':
        if user_id == ADMIN_ID:
            await query.message.reply_text("Preparing data... Please wait.")
            await send_admin_data(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    text = update.message.text
    
    if user_id == ADMIN_ID:
        return

    state = get_user_state(user_id)
    
    if state == 'ask_telegram_username':
        users_data[user_id]['telegram_username'] = text
        set_user_state(user_id, 'twitter_mission_step_1')
        
        keyboard = [[InlineKeyboardButton(get_text("follow_twitter_button"), url=LINKS['twitter_page'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_text("after_telegram_username_message"), reply_markup=reply_markup)
        
        await context.bot.send_message(chat_id=user_id, text=get_text("after_follow_twitter_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text("done_button"), callback_data='done_twitter_follow')]]))
    
    elif state == 'ask_twitter_username':
        users_data[user_id]['twitter_username'] = text
        set_user_state(user_id, 'website_mission')
        
        keyboard = [[InlineKeyboardButton(get_text("visit_website_button"), url=LINKS['website'])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(get_text("after_twitter_username_message"), reply_markup=reply_markup)
        
        await context.bot.send_message(chat_id=user_id, text=get_text("after_visit_website_message"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_text("done_button"), callback_data='done_website')]]))

    elif state == 'ask_wallet_address':
        users_data[user_id]['wallet_address'] = text
        set_user_state(user_id, 'completed')
        completed_airdrop_users.add(user_id)

        direct_count, indirect_count = get_referral_counts(user_id)
        total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
        
        thank_you_text = get_text("thank_you_message")
        
        keyboard = [
            [InlineKeyboardButton(get_text("my_tokens_button"), callback_data='my_tokens')],
            [InlineKeyboardButton(get_text("my_referral_link_button"), callback_data='my_referral_link')],
            [InlineKeyboardButton(get_text("my_referrals_button"), callback_data='my_referrals')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(thank_you_text, reply_markup=reply_markup)

    else:
        pass

async def send_admin_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id == ADMIN_ID:
        if not users_data:
            await update.message.reply_text("No user data available to export.")
            return

        output = io.StringIO()
        fieldnames = ['Telegram ID', 'Telegram Username', 'Twitter Username', 'Wallet Address', 'Referred By ID', 'Direct Referrals', 'Indirect Referrals', 'Total Tokens']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for user_id, user_info in users_data.items():
            if 'wallet_address' in user_info:
                direct_count, indirect_count = get_referral_counts(user_id)
                total_tokens = AIRDROP_TOKEN_AMOUNT + (direct_count * DIRECT_REFERRAL_BONUS) + (indirect_count * INDIRECT_REFERRAL_BONUS)
                
                writer.writerow({
                    'Telegram ID': user_id,
                    'Telegram Username': user_info.get('telegram_username', 'N/A'),
                    'Twitter Username': user_info.get('twitter_username', 'N/A'),
                    'Wallet Address': user_info.get('wallet_address', 'N/A'),
                    'Referred By ID': referred_by.get(user_id, 'N/A'),
                    'Direct Referrals': direct_count,
                    'Indirect Referrals': indirect_count,
                    'Total Tokens': total_tokens,
                })
        
        output.seek(0)
        
        await update.message.reply_document(document=output.getvalue().encode('utf-8'), filename="participants.csv")

def main() -> None:
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set!")
        return
    
    if not WEBHOOK_URL:
        logging.error("WEBHOOK_URL is not set!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the webhook server
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"/webhook/{BOT_TOKEN}",
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()