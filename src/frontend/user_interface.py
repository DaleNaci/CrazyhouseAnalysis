from src.backend.data_handler import DataHandler


starting_message = """
What would you like to do?

(1) Create a new database
"""


def run():
    action = input(starting_message)

    if action == "1":
        dh = DataHandler("src/data", "src/tables")
        dh.run()