import json
import logging
from entities.test_user import TestUser
from dbconnection import connection
import os

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

TEST_USER_FILE = os.getcwd() + "/test_users.json"


def insert_test_users(connection):
    """
    Insert test users into the database
    :return:
    """
    try:

        cursor = connection.get_connection().cursor()

        with open(TEST_USER_FILE) as file:
            test_users = json.load(file)
            file.close()
            for user in test_users:
                new_user = TestUser(user['name'], user['password'])
                logger.debug(f"Inserting new test user: {new_user}")

                new_user.insert(cursor)

                connection.get_connection().commit()

        cursor.close()


    except Exception as database_conenction_error:
        logger.debug(f"Error connecting to database: {database_conenction_error}")
        return


if __name__ == '__main__':
    connection = connection.Connection()
    insert_test_users(connection)
