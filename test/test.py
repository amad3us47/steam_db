import requests
import sqlite3


url = "https://store.steampowered.com/api/appdetails"
params = {"appids": 2017080, "cc": "gb", "l": "en"}

def get_price():
    con=sqlite3.connect("games.db")
    cur=con.cursor()
    for row in cur.execute("SELECT id, name FROM games ORDER BY id"):
        return row[0]
response = requests.get(url, params=params, timeout=15)
result = response.json()["2017080"]

if result["success"]:
    game = result["data"]
    print("Name:", game["name"])
    print("Price:", game.get("price_overview", {}).get("final_formatted", "Free or unavailable"))

if __name__=="__main__":
    cur_id=get_price()
    print(cur_id)

