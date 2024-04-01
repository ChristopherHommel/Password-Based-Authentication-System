import logging


class User:
    """
    Represents a user that could be in the system
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    salt = '123'
    test_only = False

    def __init__(self, name, password, cursor):
        self.name = name
        self.password = password
        self.cursor = cursor

    def insert(self):
        """
        Insert the user into the database
        :param cursor: cursor to the database
        :return:
        """
        self.logger.debug(f"Inserting new user: {self.name}")

        self.cursor.execute(f"INSERT INTO users "
                       f"(name, password, salt, test_only) "
                       f"VALUES "
                       f"('{self.name}', '{self.password}', '{self.salt}', {self.test_only})")

    def select(self):
        """
        Select the user from the database
        :param cursor: cursor to the database
        :return: user if a user is found, False otherwise
        """
        self.logger.debug(f"Selecting new user: {self.name}")

        self.cursor.execute(f"SELECT * FROM users WHERE name = '{self.name}'")
        user = self.cursor.fetchone()

        if user:
            return user

        else:
            return False

    def __repr__(self):
        return f"Creating new user({self.name})"

    def set_name(self, name):
        """
        Set the name of the user
        :param name: name of the user
        :return: None
        """
        self.name = name

    def set_password(self, password):
        """
        Set the password of the user
        :param password: password of the user
        :return: None
        """
        self.password = password

    def set_cursor(self, cursor):
        """
        Set the cursor of the user
        :param cursor: cursor of the user
        :return: None
        """
        self.cursor = cursor
