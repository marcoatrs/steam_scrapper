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


def filter_no_existed_games(game_ids: list[int], items: list[tuple]) -> list[tuple]:
    games = set(game_ids)
    # id, name, id_game
    print(len(items))
    new_items = list(filter(lambda i: len(i) == 3, items))
    print(len(new_items))

    new_id = [elem[0] for elem in new_items if elem[2] in games]
    new_name = [elem[1] for elem in new_items if elem[2] in games]
    new_id_game = [elem[2] for elem in new_items if elem[2] in games]
    print(len(new_id))
    return list(zip([new_id, new_name, new_id_game]))
