#THIS DEFINES SPECIFIC ACTION IN THE APPLICATION
from config import *
from models import User, Transaction, session
from datetime import date
from coinbase.wallet.client import Client

client = Client(API_KEY, API_SECRET)

# Get Primary account for querying information with API
account = client.get_accounts().data

btc_account = account[1]
xrp_account = account[0]

def get_or_create_user(message):
    """
    Returns The instance os user data
    """
    entity_id = message.from_user.id
    user = session.query(User).get(int(entity_id))
    
    if user == None:
        #Create new user
        user = create_user(message)

    return user


def create_user(message):
    """
    Create A New User To Database
    """
    entity_id = message.from_user.id

    #Generating the receive address
    btc_address = client.create_address(btc_account.id)
    xrp_address = client.create_address(xrp_account.id)

    user = User(
        id = int(entity_id),
        first_name = message.from_user.first_name,

        btc_balance = 0,
        xrp_balance = 0,

        btc_address = btc_address.address,
        xrp_address = xrp_address.address,

        btc_address_id = btc_address.id,
        xrp_address_id = xrp_address.id,

        btc_investment = 0,
        xrp_investment = 0,
        date_joined = str(date.today()),
    )
    session.add(user)
    return user


def add_btc_balance(user, amount):
    """
    Add Bitcoin To User Balance
    """
    balance = float(user.btc_balance) + float(amount)

    user.btc_balance = float(balance)
    session.add(user)


def add_xrp_balance(user, amount):
    """
    Add Ripple To User Balance
    """
    balance = float(user.xrp_balance) + float(amount)

    user.xrp_balance = float(balance)
    session.add(user)



def withdraw_btc(user, address, amount):
    """
    Sending Bitcoin To User
    """
    try:

        #Send bitcoin
        btc_account.send_money(
            to = str(address),
            amount = amount,
            currency = "BTC",
        )
        user.btc_balance -= float(amount)
        session.add(user)
        return "Payment Sent!"

    except:
        return "Unable to process payment. Please verify the address and try again!"


def withdraw_xrp(user, address, amount):
    """
    Sending Ripplecoin To User
    """
    if float(user.xrp_balance) >= float(amount):

        #Send bitcoin
        xrp_account.send_money(
            to = str(address),
            amount = amount,
            currency = "XRP",
        )
        user.xrp_balance -= float(amount)
        session.add(user)
        return "Payment Sent!"

    else:
        return "Insufficient Balance!"

def send_admin(amount, currency):
    """Send Admin Fees"""
    if currency == "BTC":
        btc_account.send_money(
            to = BTC_ADMIN_ADDRESS, # Admin wallet
            amount = str(amount),
            currency = currency,
        )
    else:
        xrp_account.send_money(
            to = XRP_ADMIN_ADDRESS, # Admin wallet
            amount = str(amount),
            currency = currency,
        )

def send_reserve(amount, currency):
    """Send To Reserve Wallet"""

    if currency == "BTC":
        address = btc_account.get_addresses()[0].address

        btc_account.send_money(
            to = address, # Reserve wallet
            amount = str(amount),
            currency = currency,
        )

    else:
        address = xrp_account.get_addresses()[0].address

        xrp_account.send_money(
            to = address, # Reserve wallet
            amount = str(amount),
            currency = currency,
        )


def send_trade(amount, currency):
    """Send To Trading Wallet"""
    if currency == "BTC":
        btc_account.send_money(
            to = BTC_TRADE_ADDRESS, # Trade wallet
            amount = str(amount),
            currency = currency,
        )
    else:
        xrp_account.send_money(
            to = XRP_TRADE_ADDRESS, # Trade wallet
            amount = str(amount),
            currency = currency,
        )


def invest_btc(user, amount):
    """
    Send Bitcoin to Refrence Points
    """
    ## Calculate fees
    fees = 0.0149 * float(amount)
    funds = float(amount) - fees

    ## Split funds by ratio
    admin_funds = 0.1 * funds
    send_admin(amount=admin_funds, currency="BTC")

    reserve_funds = 0.2 * funds
    send_reserve(amount=reserve_funds, currency="BTC")

    trade_funds = 0.7 * funds
    send_trade(amount=trade_funds, currency="BTC")

    ## Update user balance
    user.btc_investment = float(user.btc_investment) + float(funds)
    user.btc_balance = float(user.btc_balance) - float(amount)
    session.add(user)


def invest_xrp(user, amount):
    """
    Send Ripplecoin to Refrence Points
    """
    ## Calculate fees
    fees = 0.0149 * float(amount)
    funds = float(amount) - fees

    ## Split funds by ratio
    admin_funds = 0.1 * funds
    send_admin(amount=admin_funds, currency="XRP")

    reserve_funds = 0.2 * funds
    send_reserve(amount=reserve_funds, currency="XRP")

    trade_funds = 0.7 * funds
    send_trade(amount=trade_funds, currency="XRP")

    ## Update user balance
    user.xrp_investment = float(user.xrp_investment) + float(funds)
    user.xrp_balance = float(user.xrp_balance) - float(amount)
    session.add(user)

###################HISTORY####

def retrieve_transactions(user):
    """
    Update user transactions
    """
    transaction_ids = [i.id for i in user.transaction]

    # From api endpoint
    api_transaction = btc_account.get_address_transactions(user.btc_address_id).data + xrp_account.get_address_transactions(user.xrp_address_id).data 

    for each in api_transaction:

        if each.id not in transaction_ids:
            Transaction(
                id = each.id,  # Change this to transaction id
                currency = each.amount.currency,
                amount = each.amount.amount,
                title = each.details.title,
                hash = each.network.hash,
                status = each.status,
                date_created = str(date.today()),
                owner = user,
            )

            if each.details.title == "Received Bitcoin":

                user.btc_balance += float(each.amount.amount)

            elif each.details.title == "Recieved Ripplecoin":

                user.xrp_balance += float(each.amount.amount)

            else:
                pass
        else:
            pass
    
    session.add(user)


def get_transactions_history(user):
    """
    Return the list of user transactions
    """
    retrieve_transactions(user)

    history = user.transaction
    return history






























# def get_or_create_user(msg):
#     """
#     Get Or Create User
#     """
#     user = User.get_user(msg.from_user.id)
    
#     if user is None:

#         # Creating new user
#         user = User(
#             name = msg.from_user.first_name,
#             id = msg.from_user.id,
#         )

#     return user



