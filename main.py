import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from translations import get_translation as translate
import logging
import pandas as pd

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7578618644  # عدد صحیح بدون کوتیشن

# فرض بر این است که دیتا در فایل csv یا دیتابیس دارید، اینجا نمونه ساده با دیکشنری
users_data = {}

def save_data():
    # مثال ساده ذخیره داده در فایل اکسل
    df = pd.DataFrame(users_data.values())
    df.to_excel('participants.xlsx', index=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = 'en'  # اینجا می‌توانید منطق تعیین زبان را بگذارید
    text = translate(lang, 'welcome_message')
    keyboard = [
        [InlineKeyboardButton(translate(lang, 'join_telegram_button'), callback_data='join_telegram')],
        [InlineKeyboardButton(translate(lang, 'my_tokens_button'), callback_data='my_tokens')],
        [InlineKeyboardButton(translate(lang, 'my_referral_link_button'), callback_data='my_referral_link')],
        [InlineKeyboardButton(translate(lang, 'my_referrals_button'), callback_data='my_referrals')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')

# نمونه هندلر کال‌بک‌ها (باید بر اساس منطق اصلی خودت کامل کنی)
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = 'en'  # تعیین زبان طبق منطق شما

    if query.data == 'join_telegram':
        await query.message.reply_text(translate(lang, 'after_join_telegram_message'))
    elif query.data == 'my_tokens':
        # فرضاً دریافت توکن‌ها از داده‌ها
        tokens = users_data.get(user_id, {}).get('tokens', 0)
        await query.message.reply_text(translate(lang, 'my_tokens_message').format(total_tokens=tokens), parse_mode='HTML')
    elif query.data == 'my_referral_link':
        referral_link = f"https://t.me/YourBot?start={user_id}"
        await query.message.reply_text(translate(lang, 'your_referral_link_message').format(referral_link=referral_link), parse_mode='HTML')
    elif query.data == 'my_referrals':
        direct = users_data.get(user_id, {}).get('direct_referrals', 0)
        indirect = users_data.get(user_id, {}).get('indirect_referrals', 0)
        await query.message.reply_text(translate(lang, 'your_referrals_message').format(direct=direct, indirect=indirect), parse_mode='HTML')
    else:
        await query.message.reply_text("Unknown action.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    # اینجا می‌تونی منطق دریافت یوزرنیم، والت آدرس و ... رو اضافه کنی
    await update.message.reply_text("پیام دریافت شد.")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("دسترسی ندارید.")
        return
    # ایجاد فایل اکسل و ارسال به ادمین
    save_data()
    await update.message.reply_document(document=open('participants.xlsx', 'rb'))

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CommandHandler("admin", admin_command))

    application.run_polling()

if __name__ == "__main__":
    main()