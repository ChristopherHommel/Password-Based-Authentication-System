from entities.user import User


class TestUser(User):
    """
    Extends User class to represent a user that is used only for testing purposes
    """

    def __init__(self, name, password, cursor, connection):
        super().__init__(name, password, cursor, connection)
        self.test_only = True

    def __repr__(self):
        return f"Creating new test user({self.name} is test user {self.test_only})"
