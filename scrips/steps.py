import logging
from entities.user import User

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

def steps():
    """
    Asks the user for input of username and password
    :return: A new User object
    """

    user = User(None, None, None, None)

    user.set_name(input("Enter your username: "))
    user.set_password(input("Enter your password: "))

    return user
