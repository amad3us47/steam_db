import sqlite3
import requests
from bs4 import BeautifulSoup

base_url="https://store.steampowered.com/app/"
response=requests.get(base_url+str(3405340))
#print(response.text)

soup=BeautifulSoup(response.text,'html.parser')
print(soup.prettify())






con=sqlite3.connect("games.db")
cur = con.cursor()
cur.execute("CREATE TABLE games(game,id,price)")
cur.execute("""
            INSERT INTO games VALUES
            ('dota 2',37,800),
            ('genshin',22,1000)
""")
con.commit()


for row in cur.execute("SELECT price,game,id FROM games ORDER BY price"):
    print(row)
