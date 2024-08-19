import json
from pathlib import Path


_not_full_path = Path(__file__).parents[1] / "data" / "no_fullgame.json"
_backup_files = Path(__file__).parents[1] / "data" / "backups.json"


def clean_no_basegame_list(elements_in_db: list[int], games_in_db: list[int]) -> dict[str, list]:
    # No base game in db
    with open(_not_full_path, "r") as f:
        not_full_list: list[tuple[int, int]] = json.load(f)
    not_full_list_base = [i[1] for i in not_full_list]

    # items in not_full_list_base no in new_items
    new_not_valid = [i for i in not_full_list_base if i not in set(elements_in_db)]

    if len(not_full_list) != len(new_not_valid):
        # print("No changes")
        new_not_content = [i[0] for i in not_full_list if i[1] in new_not_valid]
        print(f"Removing {len(not_full_list)} -> {len(new_not_valid)}")

        with open(_not_full_path, "w") as f:
            json.dump(list(zip(new_not_content, new_not_valid)), f)
    else:
        print("No changes!")

    # Backups
    with open(_backup_files, "r") as f:
        backpus: dict[str, list] = json.load(f)

    ok_backups = {}
    for type, items in backpus.copy().items():
        # Quitar elementos ya registrados
        element_save_not = list(filter(lambda item: item[0] not in set(elements_in_db), items))
        print(f"Remove {len(items) - len(element_save_not)} already saved!")

        # Separar los que tienen juego base guardado
        ok_backups[type] = list(filter(lambda item: item[2] in set(games_in_db), element_save_not))

        # Elemento a guardar en backup
        backpus[type] = [item for item in backpus[type] if item[0] not in set(ok_backups[type])]

        print(f"Remove {len(ok_backups[type])} from {type} backup!")

    with open(_backup_files, "w") as f:
        json.dump(backpus, f, indent=2)

    return ok_backups
