import sqlite3


class Database:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        self.conn = None
        self.cursor = None
    

    def _get_table_names(self):
        self.execute("SELECT name FROM sqlite_master WHERE type='table'")

        return self.cursor.fetchall()


    def clear(self):
        try:
            for table in self._get_table_names():
                table_name = table[0]

                self.execute(f"DELETE FROM {table_name}")
                self.commit()
        except sqlite3.Error as e:
            print(e)


    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file_name)
            self.cursor = self.conn.cursor
        except sqlite3.Error as e:
            print(e)
    

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
        except sqlite3.Error as e:
            print(e)


    def commit(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)