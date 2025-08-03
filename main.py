
from flask import Flask, request
import telebot
from telebot import types
import os
import json

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

ADMIN_ID = 6328993787
CHANNEL_USERNAME = "MiokaTokenofficial"
users = {}

@app.route("/")
def home():
    return "Mioka Airdrop Bot is Running!"

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id

    if user_id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📥 Export Users", callback_data="export_users"))
        bot.send_message(user_id, "👋 Admin Panel", reply_markup=markup)
        return

    if user_id in users:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📊 My Stats", callback_data="my_stats"))
        bot.send_message(user_id, "✅ You have already joined the airdrop.", reply_markup=markup)
        return

    users[user_id] = {"step": 0, "wallet": None, "twitter": None, "telegram": None, "referrals": [], "subreferrals": []}
    bot.send_message(user_id,
        "👋 Welcome to Mioka Airdrop Bot!\n\n"
        "✅ Complete the following tasks to receive 2000 MIO tokens:\n"
        "1️⃣ Send your Telegram username\n"
        "2️⃣ Send your Twitter username\n"
        "3️⃣ Visit our Website\n"
        "4️⃣ Submit your Wallet Address\n\n"
        "💰 You will get:\n"
        "- 2000 MIO for joining\n"
        "- 500 MIO per referral\n"
        "- 100 MIO per sub-referral\n\n"
        "🌐 Website: https://miokatoken.org\n"
        "📢 Telegram: https://t.me/MiokaTokenofficial\n"
        "🐦 Twitter: https://x.com/miokatoken"
    )
    send_step_message(user_id)

def send_step_message(user_id):
    step = users[user_id]["step"]

    if step == 0:
        bot.send_message(user_id, "✅ Step 1: Please send your Telegram username (without @):")
        bot.register_next_step_handler_by_chat_id(user_id, save_telegram)
    elif step == 1:
        bot.send_message(user_id, "✅ Step 2: Please send your Twitter username (without @):")
        bot.register_next_step_handler_by_chat_id(user_id, save_twitter)
    elif step == 2:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 Visit Website", url="https://miokatoken.org"))
        markup.add(types.InlineKeyboardButton("✅ Done", callback_data="step_done"))
        bot.send_message(user_id, "✅ Step 3: Please visit our website and click Done.", reply_markup=markup)
    elif step == 3:
        bot.send_message(user_id, "✅ Step 4: Please send your BEP20 wallet address:")
        bot.register_next_step_handler_by_chat_id(user_id, save_wallet)
    elif step == 4:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📊 My Stats", callback_data="my_stats"))
        bot.send_message(user_id, "🎉 All steps completed! You can now check your stats.", reply_markup=markup)

def save_telegram(message):
    user_id = message.from_user.id
    username = message.text.strip().lstrip("@")
    users[user_id]["telegram"] = username
    users[user_id]["step"] += 1
    bot.send_message(user_id, f"✅ Telegram username saved as @{username}")
    send_step_message(user_id)

def save_twitter(message):
    user_id = message.from_user.id
    username = message.text.strip().lstrip("@")
    users[user_id]["twitter"] = username
    users[user_id]["step"] += 1
    bot.send_message(user_id, f"✅ Twitter username saved as @{username}")
    send_step_message(user_id)

@bot.callback_query_handler(func=lambda call: call.data == "step_done")
def step_done(call):
    user_id = call.from_user.id
    if user_id in users and users[user_id]["step"] < 4:
        users[user_id]["step"] += 1
        send_step_message(user_id)

def save_wallet(message):
    user_id = message.from_user.id
    wallet = message.text.strip()
    if user_id in users:
        users[user_id]["wallet"] = wallet
        users[user_id]["step"] += 1
        bot.send_message(user_id, "✅ Wallet address saved.")
        send_step_message(user_id)

@bot.callback_query_handler(func=lambda call: call.data == "my_stats")
def show_stats(call):
    user_id = call.from_user.id
    user = users.get(user_id, {})
    wallet = user.get("wallet", "Not submitted")
    telegram = user.get("telegram", "Not submitted")
    twitter = user.get("twitter", "Not submitted")
    refs = len(user.get("referrals", []))
    subrefs = len(user.get("subreferrals", []))
    total = 2000 + (refs * 500) + (subrefs * 100)
    bot.send_message(user_id, f"📊 Your Stats:\nTelegram: @{telegram}\nTwitter: @{twitter}\nWallet: {wallet}\nReferrals: {refs}\nSub-Referrals: {subrefs}\nTotal MIO: {total}")

@bot.callback_query_handler(func=lambda call: call.data == "export_users")
def export_users(call):
    if call.from_user.id != ADMIN_ID:
        bot.send_message(call.from_user.id, "❌ You are not authorized to perform this action.")
        return
    data = []
    for uid, info in users.items():
        data.append({
            "user_id": uid,
            "telegram": info.get("telegram"),
            "twitter": info.get("twitter"),
            "wallet": info.get("wallet"),
            "referrals": len(info.get("referrals", [])),
            "subreferrals": len(info.get("subreferrals", [])),
        })
    bot.send_message(call.from_user.id, f"📤 Exported Users Data:\n" + json.dumps(data, indent=2))

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
