import telebot

TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace this with your real bot token
bot = telebot.TeleBot(TOKEN)

WELCOME_MESSAGE = """
🎉 Welcome to the Mioka Airdrop! 🎉

To receive your free 2000 MIO tokens, please complete the following steps:

1. ✅ Join our Telegram channel: https://t.me/MiokaToken
2. 🐦 Follow us on Twitter: https://twitter.com/MiokaToken
3. 🌐 Visit our website: https://miokatoken.org

📨 You'll receive:
- 2000 MIO for joining
- 500 MIO per direct referral
- 100 MIO per indirect referral

🔗 Share your referral link to earn more!

Type /start to begin.
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_MESSAGE)

def start_bot():
    bot.polling(none_stop=True)