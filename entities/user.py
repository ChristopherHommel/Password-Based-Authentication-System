import logging
import os
import sqlite3

import bcrypt


class User:
    """
    Represents a user that could be in the system
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    salt = bcrypt.gensalt(16)
    pepper = '88841bc7911fd5bb99a517a2761173ad'
    test_only = False

    def __init__(self, name, password, cursor, connection):
        self.name = name
        self.password = password
        self.cursor = cursor
        self.connection = connection

    def insert(self):
        """
        Insert the user into the database safely using parameterized queries.
        """
        self.logger.debug(f"Inserting new user: {self.name}")

        try:
            self.cursor.execute("INSERT INTO users (name, password, salt, test_only) VALUES (?, ?, ?, ?)",
                                (self.name, self.password, self.salt, self.test_only))

            self.connection.commit()

        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e}")

    def select(self):
        """
        Select the user from the database safely using parameterized queries.
        """
        self.logger.debug(f"Selecting user: {self.name}")

        try:
            self.cursor.execute("SELECT * FROM users WHERE name = ?", (self.name,))
            user = self.cursor.fetchone()

            if user:
                return user

            return False

        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e}")
            return False

    def __repr__(self):
        return f"User({self.name})"

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

    def set_connection(self, connection):
        """
        Set the connection of the user
        :param connection: connection of the user
        :return: None
        """
        self.connection = connection

    def set_cursor(self, cursor):
        """
        Set the cursor of the user
        :param cursor: cursor of the user
        :return: None
        """
        self.cursor = cursor

    def set_salt(self, salt):
        """
        Set the salt of the user
        :param salt: salt of the user
        :return: None
        """
        self.salt = salt
