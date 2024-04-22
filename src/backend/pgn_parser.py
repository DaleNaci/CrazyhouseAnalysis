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
    Action: str = None
    Player: str = None
    MoveNum: int = None
    TimeTaken: int = None


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
        self.nextMoveId = -1
        self.__set_next_move_id()


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
                    self.__parse_move_list(line, g)
                    g = Game()
            
            print(f"{file_path} has been parsed.")
        
        self.db.commit()
    

    def __get_value(self, line: str) -> str:
        """
        Returns the value of a PGN line.

        If there is no value, it will return a None value.

        Args:
            line (str): A PGN line.

        Returns:
            String representing the PGN line value.
        """
        try:
            return re.findall(r'"(.*?)"', line)[0]
        except:
            return None


    def __parse_move_list(self, line: str, g: Game):
        """
        Parses a move list line from a PGN.

        Args:
            line (str): The move list line beginning with "1.".
            g (Game): The game instance that this move list is
              associated with.
        """
        move_details = re.findall(r"\d+\.\s*[^{}]+\s*\{[^\}]*?\}", line)
        time_control_sec, time_increment = map(int, g.TimeControl.split("+"))
        white_prev_time = black_prev_time = time_control_sec
        move_count = 1 # This counts TOTAL moves including both colors

        for md in move_details:
            m = Move()

            # Setting MoveId
            m.MoveId = self.__get_next_move_id()
            
            # Setting GameId
            m.GameId = g.GameId

            # Setting Move
            m.Action = md.split()[1].replace("!", "").replace("?", "")

            # Setting Player
            m.Player = "black" if "..." in md else "white"

            # Setting MoveNum
            move_count += 1
            m.MoveNum = move_count // 2

            # Setting TimeTaken
            time_str = re.search(r"\[%clk (\d+:\d+:\d+)\]", md).group(1)
            time_sec = self.__parse_time(time_str)
            
            if m.Player == "white":
                m.TimeTaken = white_prev_time - time_sec
                white_prev_time = time_sec + time_increment
            else:
                m.TimeTaken = black_prev_time - time_sec
                black_prev_time = time_sec + time_increment
            
            self.__create_move_record(m)



    def __parse_time(self, time_str: str) -> int:
        """
        Parses the time string in the format HH:MM:SS and returns the
        total seconds.

        Args:
            time_str (str): Time string in the format HH:MM:SS.
        
        Returns:
            Integer representing the number of total seconds.
        """
        hours, minutes, seconds = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60 + seconds
            
    

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
        self.db.execute(f"""
            INSERT INTO Move
                 VALUES (
                         {m.MoveId},
                         "{m.GameId}",
                         "{m.Action}",
                         "{m.Player}",
                         {m.MoveNum},
                         {m.TimeTaken}
                        );
        """)


    def __set_next_move_id(self):
        max_id = self.db.execute("""
            SELECT MAX(MoveId)
              FROM Move;
        """)[0][0]

        if not max_id:
            max_id = 0

        self.nextMoveId = max_id + 1
    

    def __get_next_move_id(self):
        self.nextMoveId += 1
        
        return self.nextMoveId - 1