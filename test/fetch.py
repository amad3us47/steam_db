import request
import sqlite3


base_url="https://store.steampowered.com/app/"

def enum(id_num):


def redirect(url):
    r=requests.get(url,allow_redirects=True)
    return r.url



con = sqlite3.connect("database.db") // connect to the database
cur=con.cursor() // to execute the commands
