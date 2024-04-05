from dbconnection import connection
from scrips.enrolment import enrol
from scrips.verification import verify
from scrips.steps import steps
import logging
import time
import sys

# Set up the logger
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

# Set the connection to the database
connection = connection.Connection()

MAX_LOGIN_ATTEMPTS = 3

def main():
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit(0)

    if sys.argv[1] == "-e" or sys.argv[1] == "--enrolment":
        user = steps()
        user.set_connection(connection.get_connection())
        user.set_cursor(connection.get_connection_cursor())
        enrolled_user = enrol(user)

    if sys.argv[1] == "-v" or sys.argv[1] == "--verification":
        user = steps()
        user.set_connection(connection.get_connection())
        user.set_cursor(connection.get_connection_cursor())
        verified_user = verify(user)

    #
    # End of command line argument parsing
    #
    if enrolled_user[0] == 0:
        print(f"{enrolled_user[2].name} has not been enrolled due to error {enrolled_user[1]}")
    else:
        print(f"{enrolled_user[2].name} has been enrolled successfully")


def usage():
    print("Usage: python main.py")
    print("Options:")
    print("  -h, --help: Display help")
    print("  -e, --enrolment: Create a new user")
    print("  -v, --verification: Login to the system")


if __name__ == "__main__":
    start_time = time.time()
    main()
    logger.debug(f"Time taken: {time.time() - start_time}")
