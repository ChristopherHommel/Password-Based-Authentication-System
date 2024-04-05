import os
import re

import bcrypt

from entities.user import User


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

    MATCH_UPPERCASE = re.compile(r'[A-Z]')
    MATCH_LOWERCASE = re.compile(r'[a-z]')
    MATCH_NUMBERS = re.compile(r'[0-9]')
    MATCH_NON_REGULAR = re.compile(r'[^a-zA-Z0-9]')

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
        self.check_against_weak_password()
        self.check_against_breach_password()
        self.check_min_and_max_length_password()
        self.check_min_3_repeated_characters()
        self.check_password_does_not_equal_username()
        self.check_user_name_in_password()
        self.find_sequential_characters()
        self.match_3_of_4_match_cases()
        self.generate_password_hash()

        return self.user

    def execute_verification(self):
        self.validate_password()

        return self.validated

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

    def check_password_does_not_equal_username(self):
        """
        Check if the password is the same as the username.
        Updates self.validated with the validation result.
        """
        if self.user.password == self.user.name:
            self.validated[0] = 0
            self.validated[1] = "password is the same as the username."

    def check_user_name_in_password(self):
        """
        Check if the username is in the password.
        Updates self.validated with the validation result.
        """
        if self.user.name in self.user.password:
            self.validated[0] = 0
            self.validated[1] = "password contains the username."

    def find_sequential_characters(self):
        """
        Find sequential characters in a password.
        Updates self.validated with the validation result.
        """
        if len(self.user.password) < 3:
            return

        for i in range(len(self.user.password) - 2):
            current_char = ord(self.user.password[i])
            next_char = ord(self.user.password[i + 1])
            next_next_char = ord(self.user.password[i + 2])

            # Check if the characters are sequentially increasing or decreasing
            if (next_char == current_char + 1 and next_next_char == next_char + 1) or \
                    (next_char == current_char - 1 and next_next_char == next_char - 1):
                self.validated[0] = 0
                self.validated[1] = (f"Password has sequential characters "
                                     f"({self.user.password[i]}, "
                                     f"{self.user.password[i + 1]}, "
                                     f"{self.user.password[i + 2]}).")
                return

    def match_3_of_4_match_cases(self):
        """
        Check if the password has at least 3 of the 4 match cases.
        Updates self.validated with the validation result.
        """
        match_cases = 0

        if self.MATCH_UPPERCASE.search(self.user.password):
            match_cases += 1
        if self.MATCH_LOWERCASE.search(self.user.password):
            match_cases += 1
        if self.MATCH_NUMBERS.search(self.user.password):
            match_cases += 1
        if self.MATCH_NON_REGULAR.search(self.user.password):
            match_cases += 1

        if match_cases < 3:
            self.validated[0] = 0
            self.validated[1] = ("password does not match 3 or more combinations of lowercase,"
                                 " uppercase number and special characters.")

    def generate_password_hash(self):
        """
        Generate a password hash.
        :return: password hash
        """
        # Ensure the password and pepper are encoded to bytes
        password = (self.user.password + self.user.pepper).encode('utf-8')

        # Use the salt directly if it's already a byte string
        salt = self.user.salt

        hashed_password = bcrypt.hashpw(password, salt)

        #
        # Set the user password to the newly generated hashed password
        #
        self.user.password = hashed_password

    def validate_password(self):
        """
        Query the database and try to rebuild the password with the supplied password in User object
        :return:
        """
        userdb = self.user.select()

        password = (self.user.password + self.user.pepper).encode('utf-8')

        # Use the salt from the database
        salt = userdb[3]

        hashed_password = bcrypt.hashpw(password, salt)

        if userdb[2] != hashed_password:
            self.validated[0] = 0
            self.validated[1] = "password does not match the one in the database."

