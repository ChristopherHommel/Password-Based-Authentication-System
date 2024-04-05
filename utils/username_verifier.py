import re
from better_profanity import profanity as pf


class UserNameVerifier:
    """
    Runs checks over a username to ensure it meets the enrolment requirements

    Uses the username part of a User object and checks it against a set of rules

    returns a new list validated with the first element being a boolean indicating if the username is valid
    and the second element being a string with the reason why the username is valid/invalid

    1 for continue, 0 for stop, i.e 1 is valid and 0 is invalid
    """

    USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
    # Base case for a username
    validated = [1, "", {}]

    MIN_LENGTH = 1
    MAX_LENGTH = 255

    def __init__(self, user, enrollment, verification):
        self.user = user
        # To keep track of the current in use User object
        self.validated[2] = self.user

        if enrollment:
            self.execute_enrollment()

        if verification:
            self.execute_verification()

    def is_validated(self):
        return self.validated

    def execute_enrollment(self):
        """
        Call to run all the checks over the username
        :return:
        """
        self.validate_username_characters()
        self.check_profanity()
        self.name_max_and_max_range_check()
        self.username_already_exists()

        return self.validated

    def execute_verification(self):
        """
        Call to run all the checks over the username
        :return:
        """
        self.validate_username_characters()
        self.check_profanity()
        self.name_max_and_max_range_check()
        self.username_not_exists()

        return self.validated

    def validate_username_characters(self):
        """
        Validate the username has the correct characters.
        Updates self.validated with the validation result.
        """
        if not (re.match(self.USERNAME_PATTERN, self.user.name)):
            self.validated[0] = 0
            self.validated[1] = "username contains invalid characters. Allowed characters are [a-z, A-Z, 0-9, _]."

    def check_profanity(self):
        """
        Check if the username contains profanity.
        Updates self.validated with the validation result.
        """
        if pf.contains_profanity(self.user.name):
            self.validated[0] = 0
            self.validated[1] = "username contains profanity."

    def name_max_and_max_range_check(self):
        """
        Check if the username is within the length range.
        Updates self.validated with the validation result.
        """
        if len(self.user.name) < self.MIN_LENGTH:
            self.validated[0] = 0
            self.validated[1] = "username is too short."

        elif len(self.user.name) > self.MAX_LENGTH:
            self.validated[0] = 0
            self.validated[1] = "username is too long."

    def username_already_exists(self):
        """
        Check if the username already exists in the database.
        Updates self.validated with the validation result.
        """
        user = self.user.select()

        if user:
            self.validated[0] = 0
            self.validated[1] = "username already exists."

    def username_not_exists(self):
        """
        Check if the username already exists in the database.
        Updates self.validated with the validation result.
        """
        user = self.user.select()

        if not user:
            self.validated[0] = 0
            self.validated[1] = "username does not exist."
