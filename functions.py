#THIS DEFINES SPECIFIC ACTION IN THE APPLICATION
from config import *
from models import User, Transaction, session
from datetime import date

client = Client(API_KEY, API_SECRET)

# Get Primary account for querying information with API
account = client.get_primary_account()

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


def get_history(user):
    """
    Returns A list Of Transaction Objects
    """
    history = user.transaction
    print(list(history))
    return history


def create_user(message):
    """
    Create A New User To Database
    """
    entity_id = message.from_user.id

    #Generating the receive address
    address = client.create_address(account.id)

    user = User(
        id = int(entity_id),
        first_name = message.from_user.first_name,
        btc_balance = 0,
        xrp_balance = 0,
        address = address,
        address_id = address.id,
        date_joined = str(date.today()),
    )
    session.add(user)
    return user


def get_transactions_info(user, action, amount):
    """
    Create Transaction From Api Info
    """

    # Generate API Transaction ID
    ###
    db_tansaction = session.query(Transaction).get(user)

    api_transaction = account.get_address_transactions(user.address_id).data

    for each in api_transaction:

        transaction = Transaction(
            transaction_id = each.id,  # Change this to transaction id
            currency = each.amount.currency,
            amount = each.amount.amount,
            title = each.details.title,
            hash = each.network.hash,
            status = each.status,
            date_created = str(date.today()),
            owner = user,
        )
        session.add(transaction)
    return transaction



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


def withdraw_btc(user, amount):
    """
    Deducting From BTC balance
    """
    balance = float(user.btc_balance)

    user.btc_balance = float(balance)
    session.add(user)


def send_btc_to_user(user):
    """
    Sending Bitcoin
    """

    pass


def invest_btc(user, amount):
    """
    Send Bitcoin to Refrence Points
    """

    ## Calculate fees

    ## Split funds by ratio

    ## Send to respective points

    ## Update user balance

    pass



        





























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



