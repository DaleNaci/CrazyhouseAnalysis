import matplotlib.pyplot as plt

from src.backend.database import Database


def main(db_file_path, move, round_limit):
    db = Database(db_file_path)
    db.connect()

    res = db.execute("""
          SELECT Action,
                 COUNT(*) AS frequency
            FROM Move
           WHERE Player = "white"
             AND MoveNum = 1
        GROUP BY Action;
    """)

    sorted_data = sorted(res, key=lambda x: x[1], reverse=True)

    for item in sorted_data:
        print(item)
    
    actions = [t[0] for t in sorted_data]
    frequencies = [t[1] for t in sorted_data] 

    plt.figure(figsize=(10, 6))
    plt.barh(actions, frequencies)
    
    plt.xlabel("Frequency")
    plt.ylabel("Moves")
    plt.title("Frequency of First Movess")
    
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()