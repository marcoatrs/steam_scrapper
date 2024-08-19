import json
from collections import deque
from pathlib import Path

import requests

_not_valid_path = Path(__file__).parents[1] / "data" / "not_valid_list.json"
_not_full_game_path = Path(__file__).parents[1] / "data" / "no_fullgame.json"

def create_no_valid_list():
    if not _not_valid_path.exists():
        with open(_not_valid_path, "w") as f:
            json.dump([], f)

def create_not_full_game():
    if not _not_full_game_path.exists():
        with open(_not_full_game_path, "w") as f:
            json.dump([], f)


def classify_games(add_id: list[int], game_name: list[str]) -> list[int]:
    items: dict[str:list] = {}
    apps = deque(zip(add_id, game_name))
    create_no_valid_list()
    with open(_not_valid_path, "r") as f:
        not_valid_list: list = json.load(f)
    create_not_full_game()
    with open(_not_full_game_path, "r") as f:
        not_full: list[tuple[int]] = json.load(f)
    not_full = [i[0] for i in not_full]

    url = "https://store.steampowered.com/api/appdetails?appids={}"
    while len(apps) > 0:
        app = apps.popleft()
        if app[0] in not_valid_list:
            continue
        if app[0] in not_full:
            continue
        app_request_result = requests.get(url.format(app[0]))
        if app_request_result.status_code != 200:
            print(f"Request status code: {app_request_result.status_code}")
            break
        data = app_request_result.json()
        try:
            item_type = data[str(app[0])]["data"]["type"]
        except Exception:
            print(data[str(app[0])].keys(), app)
            not_valid_list.append(app[0])
            continue
        try:
            if item_type != "game":
                app = (app[0], data[str(app[0])]["data"]["name"], int(data[str(app[0])]["data"]["fullgame"]["appid"]))
        except Exception:
            print(f"No fullgame: {item_type} {app}")
            not_valid_list.append(app[0])
            continue
        if not item_type in items:
            items[item_type] = []
        items[item_type].append(app)

    with open("data/classify.json", "w") as f:
        json.dump(items, f, indent=2)

    print(f"Not valid data: {len(not_valid_list)}")
    with open(_not_valid_path, "w") as f:
        json.dump(not_valid_list, f)

    print("Games saved in data/classify.json!")
    return not_valid_list
