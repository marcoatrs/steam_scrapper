import json
from collections import deque

import requests


def classify_games(add_id: list[int], game_name: list[str]) -> tuple[str]:
    items: dict[str:list] = {}
    apps = deque(zip(add_id, game_name))

    url = "https://store.steampowered.com/api/appdetails?appids={}"
    while len(apps) > 0:
        app = apps.popleft()
        app_request_result = requests.get(url.format(app[0]))
        if app_request_result.status_code != 200:
            print(f"Request status code: {app_request_result.status_code}")
            break
        data = app_request_result.json()
        try:
            item_type = data[str(app[0])]["data"]["type"]
        except Exception:
            print(data[str(app[0])].keys(), app)
            continue
        try:
            if item_type != "game":
                app = (app[0], app[1], int(data[str(app[0])]["data"]["fullgame"]["appid"]))
        except Exception:
            print(f"No fullgame: {item_type} {app}")
            continue
        if not item_type in items:
            items[item_type] = []
        items[item_type].append(app)

    with open("data/classify.json", "w") as json_file:
        json.dump(items, json_file, indent=2)

    print("Games saved in data/classify.json!")
    return tuple(items.keys())
