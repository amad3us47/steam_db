import os
import sqlite3
import time
from parse import get_game_name

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "games.db")

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, name TEXT)")
    con.commit()
    con.close()

def get_last_id():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT MAX(id) FROM games")
    last_id = cur.fetchone()[0]
    con.close()
    return last_id if last_id is not None else 0

def store_game(app_id, name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO games VALUES (?, ?)", (app_id, name))
    con.commit()
    con.close()

MAX_RUNTIME_SECONDS = 250 * 60  # stop with time to spare before the workflow's 260-min step timeout

if __name__ == "__main__":
    init_db()
    start = get_last_id()
    print(f"Resuming from ID: {start}")

    run_start = time.time()

    for app_id in range(start, 10000000):
        if time.time() - run_start > MAX_RUNTIME_SECONDS:
            print(f"Time budget reached, stopping cleanly at ID {app_id}")
            break

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
