import sqlite3
from sqlite3 import Error


class DbImpl:
    connection = None

    def __init__(self, db_file):
        self.connection = self.create_connection(db_file)

    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            if not conn:
                conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn
