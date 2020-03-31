#THIS DEFINES SPECIFIC ACTION IN THE APPLICATION
from models import User

def get_or_create_user(msg):
    """
    Get Or Create User
    """
    user = User.get_user(msg.from_user.id)
    
    if user is None:

        # Creating new user
        user = User(
            name = msg.from_user.first_name,
            id = msg.from_user.id,
        )

    return user



