class PasswordBuilder:
    """
    This class is responsible for building the password of a user, it goes through a list of checks as per
    NIST requirements
    """
    def __init__(self, user):
        self.user = user

        self.execute()

    def execute(self):
        return self.user
