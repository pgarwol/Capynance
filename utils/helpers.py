import random


def shuffle_dict(original_dict: dict) -> dict:
    """
    Shuffles the items of a dictionary.

    Parameters:
    original_dict (dict): The dictionary to shuffle.

    Returns:
    dict: A new dictionary with the items shuffled.
    """

    items = list(original_dict.items())
    random.shuffle(items)

    return dict(items)


def sort_dict_by_values_desc(original_dict: dict) -> dict:
    """
    Sorts a dictionary by its values in descending order.

    Parameters:
    original_dict (dict): The dictionary to sort.

    Returns:
    dict: A new dictionary sorted by values in descending order.
    """

    sorted_items = sorted(original_dict.items(), key=lambda item: item[1], reverse=True)
    return dict(sorted_items)
