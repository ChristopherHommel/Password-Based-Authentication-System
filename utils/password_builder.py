import os


class PasswordBuilder:
    """
    This class is responsible for building the password of a user, it goes through a list of checks as per
    NIST requirements
    """
    # Base case for a password
    validated = [1, "", {}]

    MIN_LENGTH = 8
    MAX_LENGTH = 255

    WEAK_PASSWORD_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "weakpasswords.txt")
    BREACHED_PASSWORD_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "breachedpasswords.txt")

    def __init__(self, user):
        self.user = user
        # To keep track of the current in use User object
        self.validated[2] = self.user

        self.execute()

    def is_validated(self):
        return self.validated

    def execute(self):
        self.check_against_weak_password()
        self.check_against_breach_password()
        self.check_min_and_max_length_password()
        self.check_min_3_repeated_characters()

        return self.user

    def check_against_weak_password(self):
        """
        Check if the password is weak.
        Updates self.validated with the validation result.
        """
        with open(self.WEAK_PASSWORD_FILE) as file:
            for line in file:
                stripped_line = line.strip()

                if self.user.password == stripped_line:
                    self.validated[0] = 0
                    self.validated[1] = "password is weak."
                    break

    def check_against_breach_password(self):
        """
        Check if the password is breached.
        Updates self.validated with the validation result.
        """
        with open(self.BREACHED_PASSWORD_FILE) as file:
            for line in file:
                stripped_line = line.strip()

                if self.user.password == stripped_line:
                    self.validated[0] = 0
                    self.validated[1] = "password is breached."
                    break

    def check_min_and_max_length_password(self):
        """
        Check if the password is within the length range.
        Updates self.validated with the validation result.
        """
        if len(self.user.password) < self.MIN_LENGTH:
            self.validated[0] = 0
            self.validated[1] = "password is too short."

        elif len(self.user.password) > self.MAX_LENGTH:
            self.validated[0] = 0
            self.validated[1] = "password is too long."

    def check_min_3_repeated_characters(self):
        """
        A password cannot have 3 or more repeated characters.
        Updates self.validated with the validation result.
        """
        count = 1

        for i in range(1, len(self.user.password)):
            if self.user.password[i] == self.user.password[i - 1]:
                count += 1

                if count >= 3:
                    self.validated[0] = 0
                    self.validated[1] = f"password has 3 or more repeated characters ({self.user.password[i]})."
                    return
            else:
                count = 1

