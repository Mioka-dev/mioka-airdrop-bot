
from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    bot.send_message(chat_id=chat_id, text="🎉 Mioka Airdrop is Live!")
    return "ok"

@app.route("/")
def home():
    return "Webhook is set!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
