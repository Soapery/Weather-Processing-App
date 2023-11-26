import sqlite3

class DBCM:
    """ Represents a context manager for interacting with a SQLite database. """
    def __init__(self, db_name='weather_data.db'):
        """ Initializes an instance of the DBCM class. """
        self.db_name = db_name

    def __enter__(self):
        """ Establishes a database connection and returns a cursor. """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        """ Commits and closes database connections, or rolls back changes if an exception occurs. """
        if exc_type or exc_value or traceback:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
