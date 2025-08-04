
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from utils.translation import translations
from utils.mission import register_handlers
from config import TOKEN

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Mioka Airdrop Bot is running.", 200

def start_bot():
    register_handlers(application)

if __name__ == "__main__":
    start_bot()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
