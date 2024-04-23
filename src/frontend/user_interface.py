from src.backend.data_handler import DataHandler
import src.insights.first_move_frequency as first_move_frequency
import src.insights.d4_response_frequency as d4_response_frequency
import src.insights.early_move_winrate as early_move_winrate


starting_message = """
What would you like to do?

(1) Create a new database
(2) First Move Frequencies
(3) d4 Response Frequencies
(4) Early Move Winrate
"""


def run():
    action = input(starting_message)
    db_file_path = "src/db/database.db"

    if action == "1":
        dh = DataHandler("src/data", "src/db")
        dh.run()
    if action == "2":
        first_move_frequency.main(db_file_path)
    if action == "3":
        d4_response_frequency.main(db_file_path)
    if action == "4":
        move = input("Move?\n")
        player = input("White or black?\n")
        round_limit = int(input("Round Limit?\n"))

        early_move_winrate.main(db_file_path, move, player, round_limit)