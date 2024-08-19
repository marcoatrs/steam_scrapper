import json
from pathlib import Path


_not_full_path = Path(__file__).parents[1] / "data" / "no_fullgame.json"


def clean_no_basegame_list(new_items: list[int]):
    with open(_not_full_path, "r") as f:
        not_full_list: list[tuple[int, int]] = json.load(f)
    not_full_list_base = [i[1] for i in not_full_list]

    # items in not_full_list_base no in new_items
    new_not_valid = [i for i in not_full_list_base if i not in set(new_items)]

    if len(not_full_list) == len(new_not_valid):
        print("No changes")
        return

    new_not_content = [i[0] for i in not_full_list if i[1] in new_not_valid]
    print(f"Removing {len(not_full_list)} -> {len(new_not_valid)}")

    with open(_not_full_path, "w") as f:
        json.dump(list(zip(new_not_content, new_not_valid)), f)
