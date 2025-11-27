import requests

url="https://store.steampowered.com/app/632360"

r=requests.get(url,allow_redirects=True)
print(r.url)
