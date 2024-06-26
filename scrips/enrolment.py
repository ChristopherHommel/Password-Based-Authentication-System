import logging
from utils import password_builder, username_verifier

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)


def enrol(user):
    """
    Enrol the user in the system
    :param user: User object
    :param , db_connection A connection Object to our database
    :return: validation status
    """
    validated_username = username_verifier.UserNameVerifier(user, True, False)
    validated_password = password_builder.PasswordBuilder(user, True, False)

    if validated_username.is_validated()[0] == 0:
        return validated_username.is_validated()

    if validated_password.is_validated()[0] == 0:
        return validated_password.is_validated()

    #
    # Checks have passed we can use the User to update the database
    #
    user.insert()

    return [1, "User has been enrolled successfully", user]
