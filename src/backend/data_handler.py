import os
from typing import List

from database import Database


class DataHandler:
    """This is a Data Handler class that interacts with pgn files in
    the /src/data directory.
    
    The run method of this class can be ran to turn the data files into
    a clean dataset.

    Attributes:
        data_dir: The directory path to the directory containing the
          .pgn files.
    """
    
    def __init__(self, data_dir):
        self.data_dir = data_dir


    def run(self):
        """This is the main class method that creates the datasets.
        
        Users should be calling this method.
        """
        file_names = self.__get_file_names()



    def __get_file_names(self) -> List[str]:
        """Grabs the data file names."""
        file_names = []

        try:
            for file_name in os.listdir(self.data_dir):
                file_names.append(file_name)
        except:
            print(f"Error while accessing the {self.data_dir} directory.")
        
        return file_names
    

    def __create_game_db(self, file_path: str):
        """Creates the game database file using the local Database
        class."""
        db = Database("src/db/games.db")
        db.clear()

        # TODO: Finish CREATE TABLE SQL Query
        db.exec("""
            CREATE TABLE Game (
                GameId varchar(24),
            );
        """)


    

    def __parse_pgn(self, file_path: str):
        """Parses through a pgn file to create specific games for the
        database."""