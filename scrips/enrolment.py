import logging
from entities.user import User
from utils import password_builder, username_verifier

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def enrol(User):
    """
    Enrol the user in the system
    :param User: User object
    :param , db_connection A connection Object to our database
    :return: validation status
    """
    validated_username = username_verifier.UserNameVerifier(User)

    if validated_username.is_validated()[0] == 1:
        return validated_username.is_validated()

    else:
        return validated_username.is_validated()
