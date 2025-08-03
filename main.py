
from flask import Flask, request
import telebot
from telebot import types
import os
import json

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

ADMIN_ID = 6328993787
users = {}

@app.route("/")
def home():
    return "Mioka Airdrop Bot is Running!"

@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.from_user.id

    if user_id in users:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📊 My Stats", callback_data="my_stats"))
        if user_id == ADMIN_ID:
            markup.add(types.InlineKeyboardButton("📥 Export Users", callback_data="export_users"))
        bot.send_message(user_id, "✅ You have already joined the airdrop.", reply_markup=markup)
        return

    users[user_id] = {"step": 0, "wallet": None, "referrals": [], "subreferrals": []}

    bot.send_message(user_id,
        "👋 Welcome to Mioka Airdrop Bot!\n\n"
        "✅ Complete the following tasks to receive 2000 MIO tokens:\n"
        "1️⃣ Join our Telegram Channel\n"
        "2️⃣ Follow us on Twitter\n"
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
    markup = types.InlineKeyboardMarkup()

    if step == 0:
        markup.add(types.InlineKeyboardButton("📢 Join Telegram", url="https://t.me/MiokaTokenofficial"))
        bot.send_message(user_id, "✅ Step 1: Please join our Telegram Channel. Click the button below and then press ✅ Done.", reply_markup=markup)
    elif step == 1:
        markup.add(types.InlineKeyboardButton("🐦 Follow Twitter", url="https://x.com/miokatoken"))
        bot.send_message(user_id, "✅ Step 2: Please follow us on Twitter. Click the button below and then press ✅ Done.", reply_markup=markup)
    elif step == 2:
        markup.add(types.InlineKeyboardButton("🌐 Visit Website", url="https://miokatoken.org"))
        bot.send_message(user_id, "✅ Step 3: Please visit our website. Click the button below and then press ✅ Done.", reply_markup=markup)
    elif step == 3:
        markup.add(types.InlineKeyboardButton("💼 Submit Wallet", callback_data="submit_wallet"))
        bot.send_message(user_id, "✅ Step 4: Please submit your BEP20 wallet address.", reply_markup=markup)
    elif step == 4:
        markup.add(types.InlineKeyboardButton("📊 My Stats", callback_data="my_stats"))
        if user_id == ADMIN_ID:
            markup.add(types.InlineKeyboardButton("📥 Export Users", callback_data="export_users"))
        bot.send_message(user_id, "🎉 All steps completed! You can now check your stats.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.lower() == "✅ done")
def confirm_step(message):
    user_id = message.from_user.id
    if user_id in users and users[user_id]["step"] < 4:
        users[user_id]["step"] += 1
        send_step_message(user_id)

@bot.callback_query_handler(func=lambda call: call.data == "submit_wallet")
def ask_wallet(call):
    user_id = call.from_user.id
    bot.send_message(user_id, "📝 Please send your BEP20 wallet address:")
    bot.register_next_step_handler(call.message, save_wallet)

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
    refs = len(user.get("referrals", []))
    subrefs = len(user.get("subreferrals", []))
    total = 2000 + (refs * 500) + (subrefs * 100)
    bot.send_message(user_id, f"📊 Your Stats:\nWallet: {wallet}\nReferrals: {refs}\nSub-Referrals: {subrefs}\nTotal MIO: {total}")

@bot.callback_query_handler(func=lambda call: call.data == "export_users")
def export_users(call):
    if call.from_user.id != ADMIN_ID:
        bot.send_message(call.from_user.id, "❌ You are not authorized to perform this action.")
        return
    data = []
    for uid, info in users.items():
        data.append({
            "user_id": uid,
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
