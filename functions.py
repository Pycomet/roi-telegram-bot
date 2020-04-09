#THIS DEFINES SPECIFIC ACTION IN THE APPLICATION
from models import User, session
from datetime import date


def get_or_create_user(message):
    """
    Returns The instance os user data
    """
    entity_id = message.from_user.id

    user = session.query(User.id == int(entity_id)).first()
    
    if user == None:
        #Create new user
        user = create_user(message)

    return user


def create_user(message):
    """
    Create A New User To Database
    """
    entity_id = message.from_user.id

    user = User(
        id = int(entity_id),
        first_name = message.from_user.first_name,
        btc_balance = 0,
        xrp_balance = 0,
        date_joined = str(date.today()),
        address = 'gsvgdfv467ggf7w6gwyu484784', # Create New Receive Address
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
    session.commit()


def withdraw_btc(user, amount):
    """
    Deducting From BTC balance
    """
    balance = float(user.btc_balance)

    user.btc_balance = float(balance)
    session.commit()



        





























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



