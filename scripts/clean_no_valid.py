import json

import config as cfg


def clean_no_basegame_list(elements_in_db: list[int], games_in_db: list[int]) -> dict[str, list]:
    # No base game in db
    with open(cfg.not_full_path, "r") as f:
        not_full_list: list[tuple[int, int]] = json.load(f)
    not_full_list_base = [i[1] for i in not_full_list]

    # Aun no estan en los elementos guardados
    new_not_valid = [i for i in not_full_list_base if i not in set(elements_in_db)]

    if len(not_full_list) != len(new_not_valid):
        new_not_content = [i[0] for i in not_full_list if i[1] in new_not_valid]
        print(f"Removing {len(not_full_list)} -> {len(new_not_valid)}")

        with open(cfg.not_full_path, "w") as f:
            json.dump(list(zip(new_not_content, new_not_valid)), f)
    else:
        print("No changes!")

    # Backups
    with open(cfg.backup_files, "r") as f:
        backpus: dict[str, list] = json.load(f)

    ok_backups = {}
    for table, items in backpus.copy().items():
        # Quitar elementos ya registrados
        element_save_not = list(filter(lambda item: item[0] not in set(elements_in_db), items))
        print(f"Remove {len(items) - len(element_save_not)} already saved!")

        # Separar los que tienen juego base guardado
        ok_backups[table] = list(filter(lambda item: item[2] in set(games_in_db), element_save_not))

        # Elemento a guardar en backup
        backpus[table] = [item for item in backpus[table] if item[0] not in ok_backups[table]]

        print(f"Remove {len(ok_backups[table])} from {table} backup!")

    with open(cfg.backup_files, "w") as f:
        json.dump(backpus, f, indent=2)

    return ok_backups
