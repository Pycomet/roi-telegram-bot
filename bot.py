#Importing needed libraries
import re
import telebot
from telebot import types
import emoji

from models import User
from functions import get_or_create_user

token = '1027166109:AAH-VqLwJLRNfbPegg3hqFjdxrI6z0z4oGU'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(msg):
    """
    Starting ROIPartyBot
    """

    user = get_or_create_user(msg)
    user_id = user.get_id()
    user_name = user.get_user(user_id)

    #Keyboard Setup
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    a = types.KeyboardButton(emoji.emojize("Balance  :moneybag:", use_aliases=True))
    b = types.KeyboardButton(emoji.emojize("Deposit  :inbox_tray:", use_aliases=True))
    c = types.KeyboardButton(emoji.emojize("Withdraw  :outbox_tray:", use_aliases=True))
    d = types.KeyboardButton(emoji.emojize("Invest  :briefcase:", use_aliases=True))
    e = types.KeyboardButton(emoji.emojize("History  :scroll:", use_aliases=True))
    # f = types.KeyboardButton(emoji.emojize("Support  :busts_in_silhouette:", use_aliases=True))
    f = types.KeyboardButton(emoji.emojize("Help  :bulb:", use_aliases=True))
    
    keyboard.add(a,b)
    keyboard.add(c,d)
    keyboard.add(e,f)

    bot.send_message(
        user_id,
        emoji.emojize(
            """
    :circus_tent: Hello {0}, Welcome to ROI Party Bot  :circus_tent:
            """.format(user_name),
            use_aliases=True,
        ),
        reply_markup=keyboard
    )

@bot.message_handler(regexp='^Balance')
def balance(msg):
    "Returns Balance"
    user = get_or_create_user(msg)
    user_id = user.get_id()

    btc_balance = user.get_btc_balance()
    xrp_balance = user.get_xrp_balance()

    bot.send_message(
        user_id,
        """
    Your Account Balance:

    {0} BTC
    {1} XRP
        """.format(btc_balance, xrp_balance)
    )


@bot.message_handler(regexp='^Deposit')
def deposit(msg):
    "Deposit Function"
    user = get_or_create_user(msg)
    user_id = user.get_id()

    #Keyboard Setup
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="Bitcoin(BTC)", callback_data="1")
    b = types.InlineKeyboardButton(text="Ripplecoin(XRP)", callback_data="2")
    keyboard.add(a,b)

    bot.send_message(
        user_id,
        "Please Select A Currency",
        reply_markup=keyboard,
    )

@bot.message_handler(regexp='^Withdraw')
def withdraw(msg):
    "Withdraw Functions"
    user = get_or_create_user(msg)
    user_id = user.get_id()

    #Keyboard Setup
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="Bitcoin(BTC)", callback_data="3")
    b = types.InlineKeyboardButton(text="Ripplecoin(XRP)", callback_data="4")
    keyboard.add(a,b)

    bot.send_message(
        user_id,
        "Please Select A Currency",
        reply_markup=keyboard,
    )


@bot.message_handler(regexp='^Invest')
def invest(msg):
    """
    Return Balance
    """
    user = get_or_create_user(msg)
    user_id = user.get_id()

    #Keyboard Setup
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="Bitcoin(BTC)", callback_data="5")
    b = types.InlineKeyboardButton(text="Ripplecoin(XRP)", callback_data="6")
    keyboard.add(a,b)

    bot.send_message(
        user_id,
        "Please Select A Currency",
        reply_markup=keyboard,
    )


# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    """
    Button Response
    """
    user = get_or_create_user(call)
    user_id = user.get_id()
    
    if call.data == "1":
        bot.send_message(
            user_id,
            "Send Your Bitcoin to this address --> adkjandkjandkahsdajsbdjasdh",
        )

    elif call.data == "2":
        bot.send_message(
            user_id,
            "Send Your Ripplecoin to this address --> jdfnhjfhjdfbjdbfjdfhdfjh",
        )


print("bot polling...")
bot.polling(none_stop=True)