import sqlite3
import requests
from bs4 import BeautifulSoup

base_url = "https://store.steampowered.com/app/"
headers = {"User-Agent": "Mozilla/5.0"}

def get_game_name(app_id):
    response = requests.get(base_url + str(app_id), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    game_name = soup.find(id='appHubAppName')
    return game_name.get_text(strip=True) if game_name else "Unknown"

#print(get_game_name(3405340))  
#print(get_game_name(570))      
