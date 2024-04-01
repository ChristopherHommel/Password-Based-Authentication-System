import logging
from entities.user import User
from utils import password_builder

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

def enrol(User, db_connection):
    """
    Enrol the user in the system
    :param User: User object
    :param , db_connection A connection Object to our database
    :return: True if the user is enrolled, False otherwise
    """
