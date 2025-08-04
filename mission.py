
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please select your language:\n- English 🇬🇧\n- 日本語 🇯🇵\n- Français 🇫🇷")

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
