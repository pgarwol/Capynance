from user import User
from db_keys import DB_Keys
from typing import Tuple
import json


def is_login_valid(login: str, password: str) -> Tuple[bool, str] | Tuple[bool, None]:
    with open("database.json") as db:
        data = json.load(db)

    for user in data.keys():
        user_login = data[user][DB_Keys.LOGIN_CREDENTIALS.value][DB_Keys.LOGIN.value]
        user_password = data[user][DB_Keys.LOGIN_CREDENTIALS.value][
            DB_Keys.PASSWORD.value
        ]

        if user_login == login and user_password == password:
            return True, user

    return False, None


def read_user_from_db(id: int) -> User:
    with open("database.json") as db:
        user_data = json.load(db)[str(id)]

    return User(
        id=id,
        first_name=user_data[DB_Keys.PROFILE.value][DB_Keys.FIRST_NAME.value],
        last_name=user_data[DB_Keys.PROFILE.value][DB_Keys.LAST_NAME.value],
        email=user_data[DB_Keys.PROFILE.value][DB_Keys.EMAIL.value],
    )


def save_entity() -> None: ...
