import sqlite3

def read_games():
    con = sqlite3.connect("games.db")
    cur = con.cursor()
    for row in cur.execute("SELECT id, name FROM games ORDER BY id"):
        print(f"ID: {row[0]} | Name: {row[1]}")
    con.close()

read_games()
