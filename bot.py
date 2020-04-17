#Importing needed libraries
from config import *
from keyboards import *
from functions import *

bot = telebot.TeleBot(TOKEN, threaded=True)

@bot.message_handler(commands=['start'])
def start(msg):
    """
    Starting ROIPartyBot
    """
    user = get_or_create_user(msg)
    keyboard = main_menu()

    bot.send_message(
        msg.from_user.id,
        emoji.emojize(
            """
    :circus_tent: Hello {0}, Welcome to ROI Party Bot  :circus_tent:
            """.format(user.first_name),
            use_aliases=True,
        ),
        reply_markup=keyboard
    )

    session.commit()



@bot.message_handler(regexp='^Balance')
def balance(msg):
    "Returns Balance"
    user = get_or_create_user(msg)
    bot.send_message(
        msg.from_user.id,
        """
    Your Account Balance:

    %.4f BTC
    %.4f XRP
        """ % (float(user.btc_balance), float(user.xrp_balance))
    )



@bot.message_handler(regexp='^Deposit')
def deposit(msg):
    "Deposit Function"
    user = get_or_create_user(msg)
    keyboard = deposit_keyboard()

    bot.send_message(
        msg.from_user.id,
        "Please Select A Currency",
        reply_markup=keyboard,
    )



@bot.message_handler(regexp='^Withdraw')
def withdraw(msg):
    "Withdraw Functions"
    user = get_or_create_user(msg)
    keyboard = withdraw_keyboard(btc=user.btc_balance, xrp=user.xrp_balance)

    bot.send_message(
        msg.from_user.id,
        "Please Select Balance To Withdraw From",
        reply_markup=keyboard,
    )

###########BTC WITHDRAW###########################

def btc_withdraw1(user):
    "Ask How much To Withdraw"
    question = bot.send_message(
        user.id,
        "How much do you wish to withdraw from your available balance?",
    )
    bot.register_next_step_handler(question, btc_withdraw2)


def btc_withdraw2(msg):
    """
    Checks user available balance and request if available balance enough to make payment
    """
    try:
        amount = float(msg.text)
        user = get_or_create_user(msg)

        if float(user.btc_balance) >= amount:
            bot.send_message(
                msg.from_user.id,
                emoji.emojize(
                    """
            :hourglass_flowing_sand: Processing Payment, you will be notified shortly. :hourglass:
                    """,
                    use_aliases = True,
                )
            )

            ##### SEND OUT FUNDS TO THE USER ACCOUNT

        else:
            bot.send_message(
                msg.from_user.id,
                emoji.emojize(
                    """
            :warning: Insufficient balance. Give it another shot after checking your balance.
                    """,
                    use_aliases=True,
                ),
            )

    except:
        bot.send_message(
            user.id,
            emoji.emojize(
                """
        :warning: That was a wrong input.
                """,
                use_aliases=True,
            ),
        )
    

###########XRP WITHDRAW###########################

def xrp_withdraw1(user):
    "Ask How much To Withdraw"
    question = bot.send_message(
        user.id,
        "How much do you wish to withdraw from your available balance?",
    )
    bot.register_next_step_handler(question, btc_withdraw2)


def xrp_withdraw2(msg):
    """
    Checks user available balance and request if available balance enough to make payment
    """
    try:
        amount = float(msg.text)
        user = get_or_create_user(msg)

        if float(user.btc_balance) >= amount:
            bot.send_message(
                user.id,
                emoji.emojize(
                    """
            :hourglass_flowing_sand: Processing Payment, you will be notified shortly. :hourglass:
                    """,
                    use_aliases = True,
                )
            )

            ##### SEND OUT FUNDS TO THE USER ACCOUNT

        else:
            bot.send_message(
                user.id,
                emoji.emojize(
                    """
            :warning: Insufficient balance. Give it another shot after checking your balance.
                    """,
                    use_aliases=True,
                ),
            )

    except:
        bot.send_message(
            user.id,
            emoji.emojize(
                """
        :warning: That was a wrong input.
                """,
                use_aliases=True,
            ),
        )


@bot.message_handler(regexp='^Invest')
def invest(msg):
    """
    Return Balance
    """
    user = get_or_create_user(msg)
    keyboard = invest_keyboard()

    bot.send_message(
        msg.from_user.id,
        "Please Select A Currency To Invest With ",
        reply_markup=keyboard,
    )




@bot.message_handler(regexp='^Help')
def help(msg):
    """
    Return Help Information
    """
    bot.send_message(
        msg.from_user.id,
        "Please call your mother for help. haha",
    )




@bot.message_handler(regexp='^History')
def history(msg):
    """
    Returns the list of transactions on that account
    """
    user = get_or_create_user(msg)
    transactions = get_transactions_history(user)

    bot.reply_to(
        msg,
        emoji.emojize(
            ":moneybag: LIST OF TRANSACTIONS :moneybag:",
            use_aliases=True,
        )
    )

    for transaction in transactions:

        bot.send_message(
            user.id,
            emoji.emojize(
                f"""
    {transaction.title}
Amount :point_right: {transaction.amount} {transaction.currency}
Status :point_right: {transaction.status}
Hash :point_right: {transaction.hash}
Created on ----> {transaction.date_created}
                """,
                use_aliases=True,
            ),
        )


# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    """
    Button Response
    """
    user = get_or_create_user(call)
    
    # BTC DEPOSIT
    if call.data == "1":
        bot.send_message(
            user.id,
            "Send Your Bitcoin to this address --> adkjandkjandkahsdajsbdjasdh",
        )

    # XRP DEPOSIT
    elif call.data == "2":
        bot.send_message(
            user.id,
            "Send Your Ripplecoin to this address --> jdfnhjfhjdfbjdbfjdfhdfjh",
        )

    # BTC WITHDRAW REQUEST
    elif call.data == "3":

        btc_withdraw1(user)

    # XRP WITHDRAW REQUEST
    elif call.data == "4":
        
        xrp_withdraw1(user)


print("bot polling...")

bot.polling(none_stop=True)