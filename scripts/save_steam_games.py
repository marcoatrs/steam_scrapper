import json
import os
import sys

import psycopg2
from classify import classify_games
from clean_no_valid import clean_no_basegame_list
from dotenv import load_dotenv
from filter_games import filter_games, filter_no_existed_games, get_new_games

load_dotenv()

with open("data/games.json", "r") as json_file:
    json_games: dict = json.load(json_file)

games_list: list[dict] = json_games["applist"]["apps"]

ids_list = []
names_list = []
for game_dict in games_list:
    ids_list.append(game_dict["appid"])
    names_list.append(game_dict["name"])

# DB CONNECTION
conn = psycopg2.connect(
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
)

# SAVED GAMES
ids = []
for table in ["game", "dlc", "music", "demo"]:
    with conn.cursor() as cursor:
        query = f"SELECT id FROM {os.environ['DB_SCHEMA']}.{table}"
        cursor.execute(query)
        ids.extend([i[0] for i in cursor.fetchall()])

# FILTER NEW GAMES
new_games_ids = get_new_games(ids, ids_list)
new_ids, new_games = filter_games(ids_list, names_list, new_games_ids)
if len(new_games) == 0:
    print("No new games!")
    sys.exit(0)

print(f"{len(new_games)} New games!")

# CLASSIFY
not_valid = classify_games(new_ids, new_games)

# SAVE IN DB
with open("data/classify.json", "r") as json_file:
    apps: dict[str:list] = json.load(json_file)

if len(apps) == 0:
    print("No new items")
    sys.exit()

# Game

games = apps.get("game", [])
if "game" in apps:

    print(f"### NEW game: {len(games)} ###")
    query = f"INSERT INTO {os.environ['DB_SCHEMA']}.game(id, name) VALUES(%s, %s)"
    with conn.cursor() as cursor:
        cursor.executemany(query, apps["game"])
    conn.commit()
    apps.pop("game")
else:
    print("No found game")

# Drop item without saved game
with conn.cursor() as cursor:
    query = f"SELECT id FROM {os.environ['DB_SCHEMA']}.game"
    cursor.execute(query)
    ids = [i[0] for i in cursor.fetchall()]

    for key, values in apps.items():
        print(f"Filter {key}")
        new_values = filter_no_existed_games(ids, values)
        if (len(new_values) == 0) or (len(new_values[0]) == 0):
            print(f"No new {key}")
            continue
        print(f"### NEW {key}: {len(new_values)} ###")
        query = f"INSERT INTO {os.environ['DB_SCHEMA']}.{key}(id, name, id_game) VALUES(%s, %s, %s)"
        with conn.cursor() as cursor:
            cursor.executemany(query, new_values)
        conn.commit()


clean_no_basegame_list([i[0] for i in games])
print("Games saved!")
