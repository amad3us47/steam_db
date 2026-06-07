import sqlite3
import time
from parse import get_game_name

def init_db():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, name TEXT)")
    con.commit()
    con.close()

def get_last_id():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("SELECT MAX(id) FROM games")
    last_id = cur.fetchone()[0]
    con.close()
    return last_id if last_id is not None else 0

def store_game(app_id, name):
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO games VALUES (?, ?)", (app_id, name))
    con.commit()
    con.close()

if __name__ == "__main__":
    init_db()
    start = get_last_id()
    print(f"Resuming from ID: {start}")

    for app_id in range(start, 10000000):
        try:
            name = get_game_name(app_id)
            if name != "Unknown":
                store_game(app_id, name)
                print(f"✓ {app_id} → {name}")
            else:
                print(f"✗ {app_id} → skipped")
        except Exception as e:
            print(f"✗ {app_id} → error: {e}")

        time.sleep(1)
