import os
from typing import List

from src.backend.database import Database
from src.backend.pgn_parser import PgnParser


class DataHandler:
    """This is a Data Handler class that interacts with pgn files in
    the /src/data directory.
    
    The run method of this class can be ran to turn the data files into
    a clean dataset.

    Attributes:
        data_dir: The directory path to the directory containing the
          .pgn files.
    """
    
    def __init__(self, data_dir: str, db_dir: str):
        self.data_dir = data_dir
        self.db_dir = db_dir
        self.db = Database(f"{self.db_dir}/database.db")
        self.db.connect()


    def run(self):
        """This is the main class method that creates the datasets.
        
        Users should be calling this method.
        """
        self.__reset_db()
        self.__create_game_table()
        self.__create_move_table()
        self.db.commit()

        self.__parse_pgn_files()
        
        self.db.close()
    

    def __reset_db(self):
        """
        Deletes every table
        """
        tables = self.db.execute("""
            SELECT name
              FROM sqlite_master
             WHERE type='table';
        """)

        for t in tables:
            self.db.execute(f"""
                DROP TABLE
                  IF EXISTS {t[0]}
            """)
        
        self.db.commit()
    

    def __create_game_table(self):
        """
        Creates the Game table.
        """
        self.db.execute("""
            CREATE TABLE Game (
                GameId      VARCHAR(24) PRIMARY KEY,
                WhitePlayer VARCHAR(64),
                BlackPlayer VARCHAR(64),
                WhiteElo    INT,
                BlackElo    INT,
                Termination VARCHAR(32),
                TimeControl VARCHAR(8),
                Result      VARCHAR(8)
            );
        """)

    
    def __create_move_table(self):
        """
        Creates the Move table.
        """
        self.db.execute("""
            CREATE TABLE Move (
                MoveId    INT PRIMARY KEY,
                GameId    VARCHAR(24),
                Move      VARCHAR(8),
                Player    VARCHAR(5),
                MoveNum   INT,
                TimeTaken INT,
                FOREIGN KEY (GameId) REFERENCES Game(GameId)
            );
        """)

    
    def __parse_pgn_files(self):
        """
        Parses the PGN files and inserts data from them.
        """
        file_names = self.__get_file_names()
        pgn_parser = PgnParser(self.db_dir)

        for fn in file_names:
            pgn_parser.parse(f"{self.data_dir}/{fn}")


    def __get_file_names(self) -> List[str]:
        """
        Grabs the data file names.

        Returns:
            List of strings with the names of the files.
        """
        file_names = []

        try:
            for file_name in os.listdir(self.data_dir):
                file_names.append(file_name)
        except:
            print(f"Error while accessing the {self.data_dir} directory.")
        
        return file_names