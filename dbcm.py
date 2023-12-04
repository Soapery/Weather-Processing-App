import sqlite3

class DBCM:
    """ Context Manager class for handling SQLite3 database connections. """
    def __init__(self, db_name='weather_data.sqlite'):
        """ Initializes an instance of the DBCM class. """
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """ Establishes a connection with the SQLite3 database and returns a cursor. """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print("Opened database successfully.")
            return self.conn.cursor()
        except Exception as e:
            print("Error opening DB: ", e)
            return e

    def __exit__(self, exc_type, exc_val, exc_trace):
        """ Closes connection upon completing database tasks. """
        if exc_type or exc_val or exc_trace:
            self.conn.rollback()
            print("Error occurred. Rollback executed.")
        else:
            self.conn.commit()
            print("Changes committed.")
        self.conn.close()