import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from translations import translate
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7578618644"))  # Ensure it's an integer

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {"step": "start"}
    lang = "en"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=translate("welcome", lang))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = "en"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=translate("help", lang))

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    lang = "en"

    if user_id == ADMIN_ID:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=translate("admin_panel", lang))
        return

    await context.bot.send_message(chat_id=update.effective_chat.id, text=translate("default", lang))

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()