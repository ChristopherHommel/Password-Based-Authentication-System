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

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def insert(self, cursor):
        """
        Insert the user into the database
        :param cursor: cursor to the database
        :return:
        """
        self.logger.debug(f"Inserting new user: {self.name}")

        cursor.execute(f"INSERT INTO users "
                       f"(name, password, salt, test_only) "
                       f"VALUES "
                       f"('{self.name}', '{self.password}', '{self.salt}', {self.test_only})")

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
