from dataclasses import dataclass
import re

from src.backend.database import Database


@dataclass
class Game:
    GameId: str = None
    WhitePlayer: str = None
    BlackPlayer: str = None
    WhiteElo: int = None
    BlackElo: int = None
    Termination: str = None
    TimeControl: str = None
    Result: str = None


@dataclass
class Move:
    MoveId: int = None
    GameId: str = None
    MoveNum: int = None
    TimeTaken: int = None
    Move: str = None


class PgnParser:
    """This class is utilized to parse through multi-PGN files and
    inserting the data into the SQLite3 database.
    
    The PGN files specifically being parsed are from the PGN Lichess
    database.
    """
    def __init__(self, db_dir: str):
        self.db_dir = db_dir
        self.db = Database(f"{self.db_dir}/database.db")
        self.db.connect()


    def parse(self, file_path: str):
        """
        Parses through a PGN file and inserts data into the related
        tables based on its results.

        Args:
            file_path (str): This variable is the relative file path
              to the PGN from the CWD. 
        """
        with open(file_path, "r") as f:
            g = Game()

            for line in f.readlines():
                val = self.__get_value(line)

                if line.startswith("[Site "):
                    g.GameId = val.split("/")[-1]
                elif line.startswith("[White "):
                    g.WhitePlayer = val
                elif line.startswith("[Black "):
                    g.BlackPlayer = val
                elif line.startswith("[WhiteElo "):
                    g.WhiteElo = int(val)
                elif line.startswith("[BlackElo "):
                    g.BlackElo = int(val)
                elif line.startswith("[Termination "):
                    g.Termination = val
                elif line.startswith("[TimeControl "):
                    g.TimeControl = val
                elif line.startswith("[Result "):
                    g.Result = val
                elif line.startswith("1. "):
                    self.__create_game_record(g)
                    g = Game()
                    self.__parse_move_list(line)
            
            print(f"{file_path} has been parsed.")
        
        self.db.commit()
    

    def __get_value(self, line: str) -> str:
        """
        Returns the value of a PGN line.

        If there is no value, it will return a None value.

        Args:
            line (str): A PGN line.
        """
        try:
            return re.findall(r'"(.*?)"', line)[0]
        except:
            return None

    def __parse_move_list(self, line: str):
        """
        Parses a move list line from a PGN.

        Args:
            line (str): The move list line beginning with "1.".
        """
        pass
    

    def __create_game_record(self, g: Game):
        """
        Creates a game record based on the attributes in the Game
        dataclass.

        Args:
            g (Game): Game instance with filled attributes.
        """
        self.db.execute(f"""
            INSERT INTO Game
                 VALUES (
                         "{g.GameId}",
                         "{g.WhitePlayer}",
                         "{g.BlackPlayer}",
                         {g.WhiteElo},
                         {g.BlackElo},
                         "{g.Termination}",
                         "{g.TimeControl}",
                         "{g.Result}"
                        );
        """)


    def __create_move_record(self, m: Move):
        """
        Creates a move record based on the attributes in the Move
        dataclass.

        Args:
            m (Move): Move instance with filled attributes.
        """
        pass