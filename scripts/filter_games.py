import json
from pathlib import Path

_not_full_game_path = Path(__file__).parents[1] / "data" / "no_fullgame.json"
_backup_files = Path(__file__).parents[1] / "data" / "backups.json"


def get_new_games(saved_games_ids: list[int], new_games_ids: list[int]) -> list[int]:
    only_news = set(new_games_ids) - set(saved_games_ids)
    return list(only_news)


def filter_games(
    games_ids: list[int], games_names: list[str], ids: list[int]
) -> tuple[list[int], list[str]]:

    ids_set = set(ids)
    new_ids = [id for id in games_ids if id in ids_set]
    new_games = [name for id, name in zip(games_ids, games_names) if id in ids_set]

    return new_ids, new_games


def filter_no_existed_games(
    game_ids: list[int], items: list[tuple[int, str, int]], type: str
) -> list[tuple]:
    with open(_not_full_game_path, "r") as f:
        not_full: list[tuple[int, int]] = json.load(f)
    not_full_game = [i[0] for i in not_full]
    not_full_base = [i[1] for i in not_full]

    print(f"LEN From file: {len(not_full)}")
    games = set(game_ids)
    # id, name, id_game
    new_items = list(filter(lambda i: len(i) == 3, items))

    # Los que podemos guardar
    new_id = [elem[0] for elem in new_items if elem[2] in games]
    new_name = [elem[1] for elem in new_items if elem[2] in games]
    new_id_game = [elem[2] for elem in new_items if elem[2] in games]

    # Fullgame no guardado
    # not_found = list(set([i[2] for i in new_items]).difference(set(new_id_game)))
    not_found = [i[2] for i in new_items if i[2] not in set(new_id_game)]
    not_full_base.extend(not_found)

    # Contenido sin fullgame guardado
    # not_game = list(set([i[0] for i in new_items]).difference(set(new_id)))
    not_game = [i[0] for i in new_items if i[0] not in set(new_id)]
    not_full_game.extend(not_game)

    backup_items = [item for item in new_items if item[1] not in not_full_game]
    if len(backup_items) > 0:
        print(f"Saving {len(backup_items)} elements to backup")
        with open(_backup_files, "r") as f:
            backups: dict[str, list] = json.load(f)
        if not type in backups:
            backups[type] = []
        backups[type].extend(backup_items)
        with open(_backup_files, "w") as f:
            json.dump(backups, f, indent=2)

    print(
        f"No found base game in {len(not_game)} contents. Complete miss list: {len(not_full_game)}"
    )
    with open(_not_full_game_path, "w") as f:
        json.dump(list(zip(not_full_game, not_full_base)), f, indent=2)

    return list(zip(new_id, new_name, new_id_game))
