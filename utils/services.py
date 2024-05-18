from user import User
from utils.enums import DBFields, String
import json
import random
from pathlib import Path
from typing import Tuple
from utils.exceptions import CapynanceException, Errors, Warnings

encoding = DBFields.ENCODING.value


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
    with open(
        Path(DBFields.RELATIVE_DB_PATH + DBFields.USER_DB).resolve(),
        encoding=encoding,
    ) as db:
        user_data = json.load(db)[str(id)]
    try:
        return User(
            id=id,
            profile=user_data[DBFields.PROFILE],
            calendar=user_data[DBFields.CALENDAR],
            finances=user_data[DBFields.FINANCES],
            social=user_data[DBFields.SOCIAL],
            settings=user_data[DBFields.SETTINGS],
        )
    except Exception as e:
        raise CapynanceException(Errors.USER_NOT_FOUND) from e


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


def load_db_data(db_filename: str) -> dict:
    """
    Loads data from a JSON file.

    Args:
        db_filename (str): The filename of the JSON file to load.

    Returns:
        dict: The loaded data from the file.
    """
    with open(
        Path(DBFields.RELATIVE_DB_PATH + db_filename).resolve(),
        "r",
        encoding=encoding,
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
    user_data = load_db_data(DBFields.USER_DB)
    login_data = load_db_data(DBFields.LOGIN_DB)
    new_user_id = random.randint(1, 1000)
    user_data[new_user_id] = {
        DBFields.PROFILE: {
            DBFields.FIRST_NAME: String.EMPTY,
            DBFields.LAST_NAME: String.EMPTY,
            DBFields.EMAIL: email,
        }
    }
    login_data[new_user_id] = {
        DBFields.EMAIL: email,
        DBFields.PASSWORD: password,
    }
    dump_data(user_data, DBFields.USER_DB)
    dump_data(login_data, DBFields.LOGIN_DB)


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
        encoding=encoding,
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
    return load_db_data(DBFields.USER_DB)[str(user_id)][view_name]


def append_build(content: str) -> None:
    with open("./build.log", "a", encoding=DBFields.ENCODING) as file:
        file.write(content)
