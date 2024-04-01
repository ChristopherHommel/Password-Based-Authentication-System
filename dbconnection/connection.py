import json
import mysql.connector
import logging
import os

from dbconnection.credentials import Credentials


class Connection:
    """
    Handles Connections and transactions to the database
    """

    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    DATABASE_CONNECTION_FILE = os.getcwd() + "/dbconnection/dbconfig.json"
    credentials = None
    connection = None

    def __init__(self):
        self.logger.info("Connecting to the database")

        try:
            with open(self.DATABASE_CONNECTION_FILE) as file:
                load_credentials = json.load(file)

                self.credentials = Credentials(
                    load_credentials['dbHost'],
                    load_credentials['bdName'],
                    load_credentials['dbUserName'],
                    load_credentials['dbPassword'],
                    load_credentials['dbPort'])

            file.close()

        except FileNotFoundError:
            self.logger.debug(f"{self.DATABASE_CONNECTION_FILE} not found, exiting")
            return

        try:
            self.connection = mysql.connector.connect(
                host=self.credentials.host,
                user=self.credentials.username,
                password=self.credentials.password,
                database=self.credentials.name,
                port=self.credentials.port,
                raise_on_warnings=True
            )
        except mysql.connector.Error as database_error:
            self.logger.debug(f"Error connecting to database: {database_error}")
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
        except mysql.connector.Error as database_error:
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

        except mysql.connector.Error as database_error:
            self.logger.debug(f"Error inserting data: {database_error}")
            return False

    def __repr__(self):
        """
        Print out the database we are working with
        :return: string representation of the object
        """
        return f"Connection object to {self.credentials.name} database"
