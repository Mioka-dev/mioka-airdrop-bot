from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, 
        "👋 Welcome to Mioka Airdrop Bot!\n\n"
        "✅ Complete the following tasks to receive 2000 MIO tokens:\n"
        "1️⃣ Join our Telegram Channel\n"
        "2️⃣ Follow us on Twitter\n"
        "3️⃣ Visit our Website\n\n"
        "💰 You will get:\n"
        "- 2000 MIO for joining\n"
        "- 500 MIO per referral\n"
        "- 100 MIO per sub-referral\n\n"
        "🌐 Website: https://miokatoken.org\n"
        "📢 Telegram: https://t.me/MiokaTokenofficial\n"
        "🐦 Twitter: https://x.com/miokatoken"
    )

@app.route(f"/webhook", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 403

@app.route("/")
def home():
    return "Mioka Airdrop Bot is Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
