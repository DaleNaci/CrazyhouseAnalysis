import os
from typing import List

from src.backend.database import Database


class DataHandler:
    """This is a Data Handler class that interacts with pgn files in
    the /src/data directory.
    
    The run method of this class can be ran to turn the data files into
    a clean dataset.

    Attributes:
        data_dir: The directory path to the directory containing the
          .pgn files.
    """
    
    def __init__(self, data_dir, db_dir):
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
    

    def __reset_db(self):
        """Resets every table"""
        self.db.clear()
    

    def __create_game_table(self):
        """Creates the game database file"""
        self.db.execute("""
            CREATE TABLE Game (
                GameId VARCHAR(24) PRIMARY KEY,
                WhitePlayer VARCHAR(64),
                BlackPlayer VARCHAR(64),
                WhiteElo INT,
                BlackElo INT,
                Termination VARCHAR(32),
                TimeControl VARCHAR(8),
                Result VARCHAR(8)
            );
        """)

    
    def __create_move_table(self):
        self.db.execute("""
            CREATE TABLE Move (
                MoveId INT PRIMARY KEY,
                GameId VARCHAR(24),
                MoveNum INT,
                TimeTaken INT,
                Move VARCHAR(8),
                FOREIGN KEY (GameId) REFERENCES Game(GameId)
            );
        """)

    
    def __parse_pgn_files(self):
        """Parses the PGN files and inserts data from them."""
        file_names = self.__get_file_names()

        for fn in file_names:
            self.__parse_pgn(self, f"{self.data_dir}/{fn}")


    def __parse_pgn(self, file_path):
        """Parses through a PGN file and inserts data into the related
        tables based on its results."""
        with open(file_path):
            pass



    def __get_file_names(self) -> List[str]:
        """Grabs the data file names."""
        file_names = []

        try:
            for file_name in os.listdir(self.data_dir):
                file_names.append(file_name)
        except:
            print(f"Error while accessing the {self.data_dir} directory.")
        
        return file_names