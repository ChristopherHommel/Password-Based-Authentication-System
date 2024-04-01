from dbconnection import connection

# Set the connection to the database
connection = connection.Connection()


def main():
    print(connection.__repr__())
    pass


if __name__ == "__main__":
    main()
