from user import User
from views.view import View
from utils.enums import DBFields, String, FletNames
from utils.exceptions import CapynanceException, Errors, Warnings
import os
import json
import random
from pathlib import Path
from typing import Tuple


# @TODO PG:
# checking if email is already registered
# deleting data from db after user deletes account
# better usage of dto


def flush_build_log() -> None:
    with open(
        Path(DBFields.BUILD_LOG_PATH).resolve(), "w", encoding=DBFields.ENCODING
    ) as file:
        file.write(String.EMPTY)


def is_login_valid(email: str, password: str) -> Tuple[bool, str] | Tuple[bool, None]:
    """
    Checks if the login credentials are valid.

    Args:
        email (str): The email for login.
        password (str): The password for login.

    Returns:
        Tuple[bool, str] | Tuple[bool, None]: A tuple indicating if the login is valid and the user ID if valid.
    """
    data = load_db_data(DBFields.LOGIN_DB)

    for user in data.keys():
        user_login = data[user][DBFields.EMAIL]
        user_password = data[user][DBFields.PASSWORD]

        if user_login == email and user_password == password:
            return True, user

    return False, None


def read_user_from_db(id: str | int) -> User:
    """
    Reads user data from the database based on the provided ID.

    Args:
        id (int): The ID of the user to read from the database.

    Returns:
        User: The user dto created from the retrieved data.
    """
    try:
        return User(
            id=id,
            profile=load_db_data(
                db_filepath=merge_user_db_path(user_id=id, filename=DBFields.PROFILE)
            ),
            calendar=load_db_data(
                db_filepath=merge_user_db_path(user_id=id, filename=DBFields.CALENDAR)
            ),
            finances=load_db_data(
                db_filepath=merge_user_db_path(user_id=id, filename=DBFields.FINANCES)
            ),
            settings=load_db_data(
                db_filepath=merge_user_db_path(user_id=id, filename=DBFields.SETTINGS)
            ),
            stats=load_db_data(
                db_filepath=merge_user_db_path(user_id=id, filename=DBFields.STATS)
            ),
            manual_spending=load_db_data(
                db_filepath=merge_user_db_path(user_id=id, filename=DBFields.MANUAL_SPENDING)
            ),
        )
    except Exception as e:
        raise CapynanceException(Errors.USER_NOT_FOUND) from e


def merge_user_db_path(user_id: str, filename: str) -> str:
    """
    Returns the merged path for a user's file in the database.

    Args:
        user_id (str): The user's ID.
        filename (str): The name of the file.

    Returns:
        str: The merged path for the user's file in the database.
    """
    return f"users/{user_id}/{filename}.json"


def save_user_data(user: User) -> None:
    """
    Saves user data to the database.

    Args:
        user (User): The user dto to save.

    Returns:
        None
    """
    data = load_db_data(DBFields.USER_DB)
    data[user.id] = user.serialize()
    dump_data(data, DBFields.USER_DB)


def load_db_data(db_filepath: str) -> dict:
    """
    Loads data from a JSON file.

    Args:
        db_filename (str): The filename of the JSON file to load.

    Returns:
        dict: The loaded data from the file.
    """
    print("Reading from: ", DBFields.RELATIVE_DB_PATH + db_filepath)
    with open(
        Path(DBFields.RELATIVE_DB_PATH + db_filepath).resolve(),
        "r",
        encoding=DBFields.ENCODING,
    ) as db:
        data = json.load(db)
    return data


def create_account(email: str, password: str) -> None:
    """
    Creates a new user account with the provided email and password.

    Args:
        email (str): The email of the user for the account.
        password (str): The password for the user account.

    Returns:
        None
    """
    login_data = load_db_data(DBFields.LOGIN_DB)
    new_user_id = random.randint(1, 1000)
    init_user_db(new_user_id, email)

    login_data[new_user_id] = {
        DBFields.EMAIL: email,
        DBFields.PASSWORD: password,
    }
    dump_data(login_data, DBFields.LOGIN_DB)


def init_user_db(user_id: str | int, email: str) -> None:
    """
    Initializes the user database with default profile and stats.

    Args:
        user_id (str | int): The user's ID.
        email (str): The user's email address.
    """
    users_dir = f"{DBFields.RELATIVE_DB_PATH}/users/{str(user_id)}"
    os.makedirs(
        Path(users_dir).resolve(),
        exist_ok=True,
    )
    default_profile = {
        DBFields.FIRST_NAME: String.EMPTY,
        DBFields.LAST_NAME: String.EMPTY,
        DBFields.EMAIL: email,
    }
    default_stats = {
        "hats_owned": "",
        "hat_equiped": "",
        "capy_colors_owned": "",
        "capy_color_equiped": "",
        "shirts_owned": "",
        "shirt_equiped": "",
        "life_hearts": "1",
        "capycoins": "20000",
        "level": "",
        "exp": "",
    }
    for view in View.get_instances():
        with open(Path(f"{users_dir}/{view.name}.json").resolve(), "w") as db:
            json.dump({}, db, indent=4)

    # These are not views thus they're not in View instances
    with open(Path(f"{users_dir}/{FletNames.PROFILE}.json").resolve(), "w") as db:
        json.dump(default_profile, db, indent=4)

    with open(Path(f"{users_dir}/{FletNames.STATS}.json").resolve(), "w") as db:
        json.dump(default_stats, db, indent=4)


def dump_data(data: dict, db_filename: str) -> None:
    """
    Dumps the provided data into a JSON file.

    Args:
        data (dict): The data to be dumped into the file.
        db_filename (str): The filename of the JSON file.

    Returns:
        None
    """
    with open(
        Path(DBFields.RELATIVE_DB_PATH + db_filename).resolve(),
        "w",
        encoding=DBFields.ENCODING,
    ) as db:
        json.dump(data, db)


def get_view_data(view_name: str, user_id: str | int) -> dict:
    """
    Retrieve data for a specific view associated with a user.

    Args:
        view_name (str): The name of the view to retrieve data for.
        user_id (str | int): The ID of the user.

    Returns:
        dict: The data for the specified view associated with the user.
    """
    return load_db_data(f"{DBFields.USER_DB}{str(user_id)}/{view_name}.json")
