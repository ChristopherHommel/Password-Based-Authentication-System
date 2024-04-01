import sqlite3
import logging
import os


class Connection:
    """
    Handles Connections and transactions to the database
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    real_path = os.path.realpath(__file__)
    DATABASE_CONNECTION_FILE = os.path.join(os.path.dirname(real_path), "database.db")

    credentials = None
    connection = None

    def __init__(self):
        self.logger.info("Connecting to the SQLite database")

        try:
            self.connection = sqlite3.connect(self.DATABASE_CONNECTION_FILE)
            self.logger.debug("Successfully connected to SQLite")

            cursor = self.connection.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              password TEXT NOT NULL,
                              salt TEXT NOT NULL,
                              test_only BOOLEAN NOT NULL)""")

            self.connection.commit()
            cursor.close()

        except sqlite3.Error as database_error:
            self.logger.debug(f"Error connecting to SQLite database: {database_error}")
            return

    def get_connection(self):
        """
        Get the connection to the database
        :return: connection object
        """
        return self.connection

    def close_connection(self):
        """
        Close the connection to the database
        :return: None
        """
        self.connection.close()
        self.logger.debug("Connection closed")

    def rebuild_table(self):
        """
        Rebuilds the table
        :return: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("CREATE TABLE IF NOT EXISTS users (" 
                           "id INT AUTO_INCREMENT PRIMARY KEY, "
                           "name VARCHAR(255) NOT NULL, "
                           "password VARCHAR(255) NOT NULL, "
                           "salt VARCHAR(255) NOT NULL, "
                           "test_only BOOLEAN NOT NULL)")
            cursor.close()
            return True
        except sqlite3.Error as database_error:
            self.logger.debug(f"Error rebuilding table: {database_error}")
            return False

    def rebuild_schema(self):
        """
        Rebuilds the schema
        :return: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP SCHEMA IF EXISTS " + self.credentials.name)
            cursor.execute("CREATE SCHEMA " + self.credentials.name)
            cursor.close()
            return True
        except sqlite3.Error as database_error:
            self.logger.debug(f"Error rebuilding schema: {database_error}")
            return False

    def drop_schema(self):
        """
        Drops the schema
        :return: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP SCHEMA IF EXISTS " + self.credentials.name)
            cursor.close()
            return True
        except sqlite3.Error as database_error:
            self.logger.debug(f"Error dropping schema: {database_error}")
            return False

    def drop_database(self):
        """
        Drops the database
        :return: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP DATABASE IF EXISTS " + self.credentials.name)
            cursor.close()
            return True
        except sqlite3.Error as database_error:
            self.logger.debug(f"Error dropping database: {database_error}")
            return False

    def select(self, query):
        """
        Select data from the database
        :param query: some query to select data
        :return: result of the query, False if nothing found
        """
        assert self.connection.is_connected(), "Connection is not established"
        assert query.strip().lower().startswith("select"), "Only SELECT queries are allowed"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as database_error:
            self.logger.debug(f"Error selecting data: {database_error}")
            return False

    def insert(self, query):
        """
        Insert data into the database
        :param query: some query to insert data
        :return: True if data is inserted, False otherwise
        """
        assert self.connection.is_connected(), "Connection is not established"
        assert query.strip().lower().startswith("insert"), "Only INSERT queries are allowed"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True

        except sqlite3.Error as database_error:
            self.logger.debug(f"Error inserting data: {database_error}")
            return False

    def get_connection_cursor(self):
        """
        Get the connection cursor
        :return: connection cursor
        """
        return self.connection.cursor()

    def __repr__(self):
        """
        Print out the database we are working with
        :return: string representation of the object
        """
        return f"Connection object to {self.credentials.name} database"
