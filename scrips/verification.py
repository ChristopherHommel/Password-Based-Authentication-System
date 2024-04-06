import logging
from utils import password_builder, username_verifier

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)


def verify(user):
    """
    Verify the user in the system
    :param user: User object
    :param , db_connection A connection Object to our database
    :return: The User if the user is found, False otherwise
    """

    username_verification = username_verifier.UserNameVerifier(user, False, True)
    validated_password = password_builder.PasswordBuilder(user, False, True)

    if username_verification.is_validated()[0] == 0:
        return username_verification.is_validated()

    if validated_password.is_validated()[0] == 0:
        return validated_password.is_validated()

    return [1, "", user]
