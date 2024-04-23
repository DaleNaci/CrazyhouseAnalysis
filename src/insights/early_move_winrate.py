import matplotlib.pyplot as plt

from src.backend.database import Database


def main(db_file_path, action, player, round_limit):
    db = Database(db_file_path)
    db.connect()

    res = db.execute(f"""
        SELECT Result
          FROM Game
         WHERE GameId IN (
                          SELECT GameId
                            FROM Move
                           WHERE Action = "{action}"
                                 AND Player = "{player}"
                                 AND MoveNum <= {round_limit}
                         );
    """)

    wins = ties = losses = 0

    for game in res:
        result = game[0]

        if result == "1-0":
            wins += 1
        elif result == "0-1":
            losses += 1
        else:
            ties += 1
    
    print(wins, ties, losses)