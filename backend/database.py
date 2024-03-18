import sqlite3
from typing import List, Tuple, Any


class Database:
    """This is a Database class that acts as an API for an SQLite3 Database.

    The methods in this class can be called to interact with the SQLite3
    Database, rather than having to interface with the SQLite3 library directly.

    Attributes:
        db_file_path: The file path to the database file.
        conn: The connection object that is established to connect with the
          database file.
        cursor: This is the cursor object that can directly interact with the
          database.
    """

    def __init__(self, db_file_path: str):
        self.db_file_path = db_file_path
        self.conn = None
        self.cursor = None
    

    def _get_table_names(self) -> List[Tuple]:
        """
        Retrieves the names of all tables in the database.

        Returns:
            list: A list containing the names of every table in the database.
        """
        self.execute("SELECT name FROM sqlite_master WHERE type='table'")
        
        tables = []
        
        for t in self.cursor.fetchall():
            tables.append(t[0])
        
        return tables


    def clear(self):
        """
        Clears all records from all tables in the database.
        """
        try:
            for table_name in self._get_table_names():
                self.execute(f"DELETE FROM {table_name}")
            
            self.commit()
        except sqlite3.Error as e:
            print(e)


    def connect(self):
        """
        Establishes a connection to an SQLite database.
        """
        try:
            self.conn = sqlite3.connect(self.db_file_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(e)
    

    def execute(self, sql: str) -> List[Tuple]:
        """
        Executes the specified SQL query or command.

        Args:
            sql (str): The SQL query or command to execute.
        
        Returns:
            list: A list containing the results of the query. It will return an
              empty list if the query produces no results.
        """
        try:
            self.cursor.execute(sql)

            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(e)


    def commit(self):
        """
        Commits the current transaction to make the changes permanent.
        """
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)