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


def main():
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        sys.exit(0)

    if sys.argv[1] == "-e" or sys.argv[1] == "--enrolment":
        found = enrol(steps(), connection)

    if sys.argv[1] == "-v" or sys.argv[1] == "--verification":
        user = verify(steps(), connection)

    pass


def usage():
    print("Usage: python main.py")
    print("Options:")
    print("  -h, --help: Display help")
    print("  -e, --enrolment: Create a new user")
    print("  -v, --verification: Login to the system")


if __name__ == "__main__":
    main()
