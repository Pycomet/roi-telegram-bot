from config import *

def main_menu():
    "Return Main Menu Keyboard"

    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    a = types.KeyboardButton(emoji.emojize("Balance  :moneybag:", use_aliases=True))
    b = types.KeyboardButton(emoji.emojize("Deposit  :inbox_tray:", use_aliases=True))
    c = types.KeyboardButton(emoji.emojize("Withdraw  :outbox_tray:", use_aliases=True))
    d = types.KeyboardButton(emoji.emojize("Invest  :briefcase:", use_aliases=True))
    e = types.KeyboardButton(emoji.emojize("Help  :bulb:", use_aliases=True))
    f = types.KeyboardButton(emoji.emojize("History  :book:", use_aliases=True))
    
    keyboard.add(a,b)
    keyboard.add(c,d)
    keyboard.add(e, f)

    return keyboard


def deposit_keyboard():
    "Return Coin List"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="Bitcoin(BTC)", callback_data="1")
    b = types.InlineKeyboardButton(text="Ripplecoin(XRP)", callback_data="2")
    keyboard.add(a,b)

    return keyboard



def withdraw_keyboard(btc, xrp):
    "Return Coin Option"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="Bitcoin(BTC) Balance --> %.4f" % (float(btc)), callback_data="3")
    b = types.InlineKeyboardButton(text="Ripplecoin(XRP) Balance --> %.4f" % (float(xrp)), callback_data="4")
    keyboard.add(a,b)

    return keyboard



def invest_keyboard():
    "Return Options"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="Bitcoin(BTC) Balance", callback_data="5")
    b = types.InlineKeyboardButton(text="Ripplecoin(XRP) Balance", callback_data="6")
    keyboard.add(a,b)

    return keyboard

    