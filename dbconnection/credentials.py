class Credentials:
    """
    Holds information about a database connection
    """

    def __init__(self, host, name, username, password, port):
        self.host = host
        self.name = name
        self.username = username
        self.password = password
        self.port = port

    def __repr__(self):
        """
        String representation of the object
        :return: String
        """
        return f"Connecting on : ({self.name}, using {self.host} over port {self.port})"
