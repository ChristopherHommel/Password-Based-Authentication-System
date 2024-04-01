Password-Based-Authentication-System

# Components
Python 3.7, MySQL


# Installation
    MYSQL:
        1. Create a new MYSQL connection with the name Password-Based-Authentication-System
        2. Create a new schema with the name password_based_authentication_system
            2.1 Default Charset
            2.2 Default Collation
            2.3 Apply
            2.4 Finish

    Python:
        1. Install packages found in requirements.txt
            1.1 pip install -r requirements.txt

# Usage

# Test
    Running the main script will insert test rows into the database where their columns will have `test_only`
    which can be used to query test data. Any user entered data will have this row set to false.
