from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv
import os
from translation import t

API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

users_file = 'users.csv'

def get_user_ids():
    if not os.path.isfile(users_file):
        return []
    with open(users_file, newline='') as f:
        return [row[0] for row in csv.reader(f)]

def save_user(user_id):
    user_id = str(user_id)
    users = get_user_ids()
    if user_id not in users:
        with open(users_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user_id])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.chat.id)
    save_user(user_id)

    if str(user_id) == str(ADMIN_ID):
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(t("Broadcast", "en"), callback_data="broadcast"))
        markup.row(InlineKeyboardButton(t("Users", "en"), callback_data="users"))
        markup.row(InlineKeyboardButton(t("Stats", "en"), callback_data="stats"))
        markup.row(InlineKeyboardButton(t("Export CSV", "en"), callback_data="export"))
        bot.send_message(user_id, "Admin Panel:", reply_markup=markup)
    else:
        # پیام خوش‌آمدگویی برای کاربر عادی
        bot.send_message(user_id, t("Welcome", "en"))

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if str(call.message.chat.id) != str(ADMIN_ID):
        return

    if call.data == "broadcast":
        bot.send_message(ADMIN_ID, t("Send the message you want to broadcast", "en"))
        bot.register_next_step_handler_by_chat_id(ADMIN_ID, process_broadcast)

    elif call.data == "users":
        users = get_user_ids()
        bot.send_message(ADMIN_ID, t("Total Users", "en") + f": {len(users)}")

    elif call.data == "stats":
        stats_text = f"{t('Total Users', 'en')}: {len(get_user_ids())}"
        bot.send_message(ADMIN_ID, stats_text)

    elif call.data == "export":
        if not os.path.isfile(users_file):
            bot.send_message(ADMIN_ID, t("No users to export", "en"))
            return

        with open(users_file, 'rb') as f:
            bot.send_document(ADMIN_ID, f, caption="users.csv")

def process_broadcast(message):
    text = message.text
    users = get_user_ids()
    count = 0
    for user_id in users:
        try:
            bot.send_message(user_id, text)
            count += 1
        except Exception:
            pass
    bot.send_message(ADMIN_ID, f"{t('Message sent to', 'en')} {count} {t('users', 'en')}")

@app.route('/')
def index():
    return 'Bot is running.'

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{os.getenv('RENDER_URL')}/{API_TOKEN}")

if __name__ == '__main__':
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
