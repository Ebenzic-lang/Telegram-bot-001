import os
from flask import Flask
from threading import Thread
import telebot
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

TOKEN = "8775829572:AAFjk7qEfh5-J3DMXDFrVD2gLJQ3TwKs6pg"
CHANNEL_USERNAME = "@Vipwinningsignals"  # e.g @vipalerts

bot = telebot.TeleBot(TOKEN)

def check_user(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    join_btn = telebot.types.InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")
    check_btn = telebot.types.InlineKeyboardButton("🔓 I Joined (Unlock)", callback_data="check")

    markup.add(join_btn)
    markup.add(check_btn)

    bot.send_message(
        message.chat.id,
        "Welcome 👋\nGet access to exclusive drops + winner alerts.\n\nStep 1/2: Join our channel to unlock.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "check":
        if check_user(call.from_user.id):

            markup = telebot.types.InlineKeyboardMarkup()
            play_btn = telebot.types.InlineKeyboardButton("🎰 Play Now", url="https://t.me/gemzcoin_bot/playfun?startapp=eyJzIjoidGVsZWdyYW0iLCJtIjoiYm90IiwiZiI6ImJyb2FkY2FzdCJ9")
            offer_btn = telebot.types.InlineKeyboardButton("🎁 Today’s Offer", callback_data="offer")
            support_btn = telebot.types.InlineKeyboardButton("💬 Support", url="https://t.me/Vipwinningsignals")

            markup.add(play_btn)
            markup.add(offer_btn)
            markup.add(support_btn)

            bot.edit_message_text(
                "Unlocked 🎉\nStep 2/2: Continue to the site.",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )

        else:
            markup = telebot.types.InlineKeyboardMarkup()
            join_btn = telebot.types.InlineKeyboardButton("✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")
            retry_btn = telebot.types.InlineKeyboardButton("🔓 Try Unlock Again", callback_data="check")

            markup.add(join_btn)
            markup.add(retry_btn)

            bot.answer_callback_query(call.id, "You must join first!")

            bot.send_message(
                call.message.chat.id,
                "Not subscribed yet — join to unlock access.\n\n⚡ Daily winning signals\n🎁 Exclusive bonuses\n🔥 Limited drops",
                reply_markup=markup
            )

    elif call.data == "offer":
        markup = telebot.types.InlineKeyboardMarkup()
        play_btn = telebot.types.InlineKeyboardButton("🎰 Play Now", url="https://t.me/gemzcoin_bot/playfun?startapp=eyJzIjoidGVsZWdyYW0iLCJtIjoiYm90IiwiZiI6ImJyb2FkY2FzdCJ9")
        back_btn = telebot.types.InlineKeyboardButton("🔙 Back", callback_data="check")

        markup.add(play_btn)
        markup.add(back_btn)

        bot.edit_message_text(
            "🎁 Today’s Exclusive Bonus\n\nGet a special reward when you sign up today.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
keep_alive()
bot.infinity_polling()
