import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from translations import get_translation as translate
import os
import pandas as pd

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Admin Telegram ID
ADMIN_ID = 7578618644  # Make sure this is an integer

# Load environment variables
TOKEN = os.environ.get("BOT_TOKEN")

# DataFrame to store user data
data = pd.DataFrame(columns=["user_id", "telegram_username", "twitter_username", "wallet_address", "referrer"])

# Function to get user's language or default to English
def get_user_language(update: Update) -> str:
    if update.effective_user.id == ADMIN_ID:
        return 'en'
    if update.effective_user.language_code in ['en', 'jp', 'fr']:
        return update.effective_user.language_code
    return 'en'

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(update)

    if user_id == ADMIN_ID:
        keyboard = [[InlineKeyboardButton("📊 Export Data", callback_data="export")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Admin Panel:", reply_markup=reply_markup)
        return

    # Check if user already exists
    if user_id in data['user_id'].values:
        await update.message.reply_text(translate(lang, 'already_joined_message'))
        return

    keyboard = [[InlineKeyboardButton(translate(lang, 'join_telegram_button'), url="https://t.me/YourChannel")],
                [InlineKeyboardButton(translate(lang, 'done_button'), callback_data="joined")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(translate(lang, 'welcome_message'), reply_markup=reply_markup)

# Callback query handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(update)

    if user_id == ADMIN_ID and query.data == "export":
        file_path = "/tmp/airdrop_data.xlsx"
        data.to_excel(file_path, index=False)
        with open(file_path, 'rb') as f:
            await context.bot.send_document(chat_id=ADMIN_ID, document=f, filename="airdrop_data.xlsx")
        return

    if query.data == "joined":
        await query.edit_message_text(text=translate(lang, 'after_join_telegram_message'))
        await context.bot.send_message(chat_id=user_id, text=translate(lang, 'enter_telegram_username'))
        context.user_data['step'] = 'telegram_username'

# Message handler to collect user inputs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(update)
    text = update.message.text

    if user_id == ADMIN_ID:
        await update.message.reply_text("This bot is live and working properly.")
        return

    step = context.user_data.get('step')

    if step == 'telegram_username':
        context.user_data['telegram_username'] = text
        context.user_data['step'] = 'twitter_username'
        keyboard = [[InlineKeyboardButton(translate(lang, 'follow_twitter_button'), url="https://twitter.com/YourProfile")],
                    [InlineKeyboardButton(translate(lang, 'done_button'), callback_data="followed")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(translate(lang, 'after_telegram_username_message'), reply_markup=reply_markup)

    elif step == 'twitter_username':
        context.user_data['twitter_username'] = text
        context.user_data['step'] = 'wallet_address'
        keyboard = [[InlineKeyboardButton(translate(lang, 'visit_website_button'), url="https://yourwebsite.com")],
                    [InlineKeyboardButton(translate(lang, 'done_button'), callback_data="visited")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(translate(lang, 'after_twitter_username_message'), reply_markup=reply_markup)

    elif step == 'wallet_address':
        context.user_data['wallet_address'] = text
        context.user_data['step'] = None

        # Save to DataFrame
        new_row = {
            "user_id": user_id,
            "telegram_username": context.user_data.get('telegram_username'),
            "twitter_username": context.user_data.get('twitter_username'),
            "wallet_address": context.user_data.get('wallet_address'),
            "referrer": None  # Add logic if needed
        }
        global data
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

        await update.message.reply_text(translate(lang, 'thank_you_message'))

# Main function to run the bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhook settings (for Render, etc.)
    PORT = int(os.environ.get("PORT", 8443))
    URL = os.environ.get("WEBHOOK_URL")  # Make sure to set this in your environment

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{URL}/{TOKEN}"
    )

if __name__ == '__main__':
    main()
