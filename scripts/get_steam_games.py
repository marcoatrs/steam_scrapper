import json

import requests

# GET GAMES JSON
steam_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
json_games: dict = requests.get(steam_url).json()

with open("data/games.json", "w") as json_file:
    json.dump(json_games, json_file)

print("New games saved 'data/games.json'")
