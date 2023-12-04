import sqlite3
from sqlite3 import Error
from contextlib import contextmanager

class DbImpl:
    conn = None

    def __init__(self, db_file):
        self.db_file = db_file


    @contextmanager
    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = sqlite3.connect(self.db_file)
        yield self.conn
        self.conn.close()
