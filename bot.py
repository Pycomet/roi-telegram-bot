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
        "Please paste the wallet you wish to receive the funds?",
    )
    bot.register_next_step_handler(question, btc_withdraw2)


def btc_withdraw2(msg):
    """
    Receive address and pay to address
    """
    try:
        address = float(msg.text)
        user = get_or_create_user(msg)
        amount = user.btc_balance

        bot.send_message(
            user.id,
            emoji.emojize(
                """
        :hourglass_flowing_sand: Processing Payment, you will be notified shortly.

                """,
                use_aliases = True,
            )
        )

        ##### SEND OUT FUNDS TO THE USER ACCOUNT
        status = withdraw_btc(user=user, address=address, amount=amount)

        bot.send_message(
            user.id,
            "%s" % (status,),

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
    Receive address and pay to address
    """
    try:
        address = float(msg.text)
        user = get_or_create_user(msg)
        amount = user.xrp_balance

        bot.send_message(
            user.id,
            emoji.emojize(
                """
        :hourglass_flowing_sand: Processing Payment, you will be notified shortly.

                """,
                use_aliases = True,
            )
        )

        ##### SEND OUT FUNDS TO THE USER ACCOUNT
        status = withdraw_xrp(user=user, address=address, amount=amount)

        bot.send_message(
            user.id,
            "%s" % (status,),

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


########################################################################

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

###########BTC INVEST######
def invest_btc1(msg):
    """Invest Amount"""
    amount = msg.text
    user = get_or_create_user(msg)

    if float(user.btc_balance) >= float(amount):

        invest_btc(user=user, amount=amount)

        bot.send_message(
            user.id,
            "Congratulations, your account has been added to the investors list to recieve 1% daily (Monday - Friday)"
        )

        ## Add to list for admin payout

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

###########XRP INVEST######
def invest_xrp1(msg):
    """Invest Amount"""
    amount = msg.text
    user = get_or_create_user(msg)

    if float(user.xrp_balance) >= float(amount):

        invest_xrp(user=user, amount=amount)

        bot.send_message(
            user.id,
            "Congratulations, your account has been added to the investors list to recieve 1% daily (Monday - Friday)"
        )

        ## Add to list for admin payout

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


@bot.message_handler(commands=['payout'])
def payout(msg):
    """
    handler accessed by only admin to payout funds to the investors daily
    """
    user = get_or_create_user(msg)
    keyboard = authorize_payouts()

    # Get authorization
    if user.is_admin == True:
        
        bot.send_message(
            user.id,
            "Click on the buttons to send out today's ROI",
            reply_markup=keyboard,
        )

    else:
        bot.send_message(
            user.id,
            emoji.emojize(
                "Sorry {user.first_name}, you are not authorized to use this command :thumbs_down:",
                use_aliases = True,
            )
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
            "Send Your Bitcoin to this address --> %s" % (user.btc_address),
        )

    # XRP DEPOSIT
    elif call.data == "2":
        bot.send_message(
            user.id,
            "Send Your Ripplecoin to this address --> %s" % (user.xrp_address),
        )

    # BTC WITHDRAW REQUEST
    elif call.data == "3":

        btc_withdraw1(user)

    # XRP WITHDRAW REQUEST
    elif call.data == "4":
        
        xrp_withdraw1(user)

    # BTC INVEST REQUEST
    elif call.data == "5":
        
        question = bot.send_message(
            user.id,
            emoji.emojize(
                ":money_bag: How much BTC do you wish to invest?",
                use_aliases=True
            ),
        )
        bot.register_next_step_handler(question, invest_btc1)

    # XRP INVEST REQUEST
    elif call.data == "6":

        question = bot.send_message(
            user.id,
            emoji.emojize(
                ":money_bag: How much XRP do you wish to invest?",
                use_aliases=True
            ),
        )
        bot.register_next_step_handler(question, invest_xrp1)

    # MAKE ROI PAYMENTS
    elif call.data == "7":

        investors = get_investors("BTC")

        for investor in investors:
            payout_to_investor(user=investor, currency="BTC")

            bot.send_message(
                investor.id,
                emoji.emojize(
                    ":money_bag: Bitcoin ROI Received :money_bag:",
                    use_aliases=True
                )
            )


        bot.send_message(
            user.id,
            emoji.emojize(
                ":money_bag: :money_bag: Party Bot Bitcoin ROI Gifts Delivered Successfully :thumbs_up:",
                use_aliases = True,
            )
        )

    elif call.data == "8":

        investors = get_investors("XRP")

        for investor in investors:
            payout_to_investor(user=investor, currency="XRP")

            bot.send_message(
                investor.id,
                emoji.emojize(
                    ":money_bag: Ripplecoin ROI Received :money_bag:",
                    use_aliases=True
                )
            )


        bot.send_message(
            user.id,
            emoji.emojize(
                ":money_bag: :money_bag: Party Bot Ripplecoin ROI Gifts Delivered Successfully :thumbs_up:",
                use_aliases = True,
            )
        )

    else:
        pass

