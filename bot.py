
import telebot
from telebot import types

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
ADMIN_USERNAME = '@MiokaToken'

bot = telebot.TeleBot(API_TOKEN)

user_data = {}
referrals = {}

def is_registered(user_id):
    return user_id in user_data and user_data[user_id].get("completed", False)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if message.from_user.username == ADMIN_USERNAME.strip('@'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('📥 Export Users')
        bot.send_message(user_id, "Admin Panel", reply_markup=markup)
        return

    if is_registered(user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("💰 My Balance", "👥 My Referrals", "🔗 Referral Link")
        bot.send_message(user_id, "You already joined the airdrop.", reply_markup=markup)
        return

    user_data[user_id] = {"step": "telegram"}
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Telegram", url="https://t.me/MiokaTokenofficial"))
    markup.add(types.InlineKeyboardButton("✅ Done", callback_data="telegram_done"))
    bot.send_message(user_id, "👋 Welcome to Mioka Airdrop!

Complete the tasks to earn MIO tokens.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    if call.data == "telegram_done":
        bot.send_message(user_id, "✏️ Please enter your Telegram ID (e.g. @username):")
        user_data[user_id]["step"] = "enter_telegram_id"

    elif call.data == "twitter_done":
        bot.send_message(user_id, "✏️ Please enter your Twitter ID (e.g. @handle):")
        user_data[user_id]["step"] = "enter_twitter_id"

    elif call.data == "visit_site":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Done", callback_data="site_done"))
        bot.send_message(user_id, "Click Done after visiting the website.", reply_markup=markup)

    elif call.data == "site_done":
        bot.send_message(user_id, "💳 Please enter your BNB Smart Chain wallet address:")
        user_data[user_id]["step"] = "enter_wallet"

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text == "📥 Export Users" and message.from_user.username == ADMIN_USERNAME.strip('@'):
        export = "user_id,telegram_id,twitter_id,wallet\n"
        for uid, data in user_data.items():
            export += f"{uid},{data.get('telegram_id','')},{data.get('twitter_id','')},{data.get('wallet','')}\n"
        bot.send_message(user_id, f"```
{export}
```", parse_mode="Markdown")
        return

    if user_id not in user_data:
        bot.send_message(user_id, "Please type /start to begin.")
        return

    step = user_data[user_id].get("step")

    if step == "enter_telegram_id":
        user_data[user_id]["telegram_id"] = text
        user_data[user_id]["step"] = "twitter"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🐦 Follow on Twitter", url="https://x.com/miokatoken"))
        markup.add(types.InlineKeyboardButton("✅ Done", callback_data="twitter_done"))
        bot.send_message(user_id, "Great! Now follow us on Twitter.", reply_markup=markup)

    elif step == "enter_twitter_id":
        user_data[user_id]["twitter_id"] = text
        user_data[user_id]["step"] = "visit_site"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 Visit Website", url="https://miokatoken.org", callback_data="visit_site"))
        bot.send_message(user_id, "Please visit our website:", reply_markup=markup)

    elif step == "enter_wallet":
        user_data[user_id]["wallet"] = text
        user_data[user_id]["completed"] = True
        user_data[user_id]["referrals"] = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("💰 My Balance", "👥 My Referrals", "🔗 Referral Link")
        bot.send_message(user_id, "✅ You’ve successfully joined the airdrop!", reply_markup=markup)

    elif text == "💰 My Balance":
        bot.send_message(user_id, "💰 You have 2000 MIO + referral bonuses.")

    elif text == "👥 My Referrals":
        count = referrals.get(user_id, 0)
        bot.send_message(user_id, f"👥 You have {count} referral(s).")

    elif text == "🔗 Referral Link":
        bot.send_message(user_id, f"🔗 Share this link: https://t.me/MiokaAirdropBot?start={user_id}")

def run_bot():
    bot.infinity_polling()
