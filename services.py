from user import User
from utils.db_keys import DB_Keys
from utils.global_enums import String
import json
import random
from typing import Tuple
from pathlib import Path


def is_login_valid(email: str, password: str) -> Tuple[bool, str] | Tuple[bool, None]:
    """
    Checks if the login credentials are valid.

    Args:
        email (str): The email for login.
        password (str): The password for login.

    Returns:
        Tuple[bool, str] | Tuple[bool, None]: A tuple indicating if the login is valid and the user ID if valid.
    """
    data = load_db_data(DB_Keys.LOGIN_DB.value)

    for user in data.keys():
        user_login = data[user][DB_Keys.EMAIL.value]
        user_password = data[user][DB_Keys.PASSWORD.value]

        if user_login == email and user_password == password:
            return True, user

    return False, None


def read_user_from_db(id: int) -> User:
    """
    Reads user data from the database based on the provided ID.

    Args:
        id (int): The ID of the user to read from the database.

    Returns:
        User: The user dto created from the retrieved data.
    """
    with open(Path(DB_Keys.USER_DB.value)) as db:
        user_data = json.load(db)[str(id)]

    return User(
        id=id,
        first_name=user_data[DB_Keys.PROFILE.value][DB_Keys.FIRST_NAME.value],
        last_name=user_data[DB_Keys.PROFILE.value][DB_Keys.LAST_NAME.value],
        email=user_data[DB_Keys.PROFILE.value][DB_Keys.EMAIL.value],
    )


def save_user_data(user: User) -> None:
    """
    Saves user data to the database.

    Args:
        user (User): The user dto to save.

    Returns:
        None
    """
    data = load_db_data(DB_Keys.USER_DB.value)
    data[user.id] = user.serialize()
    dump_data(data, DB_Keys.USER_DB.value)


def load_db_data(db_filename: str) -> dict:
    """
    Loads data from a JSON file.

    Args:
        db_filename (str): The filename of the JSON file to load.

    Returns:
        dict: The loaded data from the file.
    """
    with open(Path(db_filename), "r") as db:
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
    user_data = load_db_data(DB_Keys.USER_DB.value)
    login_data = load_db_data(DB_Keys.LOGIN_DB.value)
    new_user_id = random.randint(1, 1000)
    user_data[new_user_id] = {
        DB_Keys.PROFILE.value: {
            DB_Keys.FIRST_NAME.value: String.EMPTY.value,
            DB_Keys.LAST_NAME.value: String.EMPTY.value,
            DB_Keys.EMAIL.value: email,
        }
    }
    login_data[new_user_id] = {
        DB_Keys.EMAIL.value: email,
        DB_Keys.PASSWORD.value: password,
    }
    dump_data(user_data, DB_Keys.USER_DB.value)
    dump_data(login_data, DB_Keys.LOGIN_DB.value)


def dump_data(data: dict, db_filename: str) -> None:
    """
    Dumps the provided data into a JSON file.

    Args:
        data (dict): The data to be dumped into the file.
        db_filename (str): The filename of the JSON file.

    Returns:
        None
    """
    with open(Path(db_filename), "w") as db:
        json.dump(data, db)
