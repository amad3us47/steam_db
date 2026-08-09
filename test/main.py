import os
import sqlite3
import time
from parse import get_game_name

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "games.db")
PROGRESS_PATH = os.path.join(BASE_DIR, "progress.txt")

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, name TEXT)")
    con.commit()
    con.close()

def get_last_id():
    # Track progress in a separate file, independent of the games table.
    # The games max id only moves when a hit is found; this counter advances on every id.
    try:
        with open(PROGRESS_PATH) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def set_last_id(app_id):
    with open(PROGRESS_PATH, "w") as f:
        f.write(str(app_id))

def store_game(app_id, name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO games VALUES (?, ?)", (app_id, name))
    con.commit()
    con.close()

MAX_RUNTIME_SECONDS = 250 * 60  # stop with time to spare before the workflow's 260-min step timeout

def seed_progress_if_missing():
    # One-time bootstrap: if there's no progress file yet but games already exist,
    # start from the highest known id instead of rescanning from zero.
    if not os.path.exists(PROGRESS_PATH):
        con = sqlite3.connect(DB_PATH)
        max_id = con.execute("SELECT MAX(id) FROM games").fetchone()[0] or 0
        con.close()
        set_last_id(max_id)

if __name__ == "__main__":
    init_db()
    seed_progress_if_missing()
    start = get_last_id() + 1
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
            set_last_id(app_id)
        except Exception as e:
            print(f"✗ {app_id} → error: {e}")

        time.sleep(1)
