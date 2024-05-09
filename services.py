from user import User
from db_keys import DB_Keys
from typing import Tuple, LiteralString
import json
import random


def is_login_valid(email: str, password: str) -> Tuple[bool, str] | Tuple[bool, None]:
    data = load_db_data(DB_Keys.LOGIN_DB.value)

    for user in data.keys():
        user_login = data[user][DB_Keys.EMAIL.value]
        user_password = data[user][DB_Keys.PASSWORD.value]

        if user_login == email and user_password == password:
            return True, user

    return False, None


def read_user_from_db(id: int) -> User:
    with open(DB_Keys.USER_DB.value) as db:
        user_data = json.load(db)[str(id)]

    return User(
        id=id,
        first_name=user_data[DB_Keys.PROFILE.value][DB_Keys.FIRST_NAME.value],
        last_name=user_data[DB_Keys.PROFILE.value][DB_Keys.LAST_NAME.value],
        email=user_data[DB_Keys.PROFILE.value][DB_Keys.EMAIL.value],
    )


def save_user_data(user: User) -> None:
    data = load_db_data(DB_Keys.USER_DB.value)
    data[user.id] = user.serialize()
    dump_data(data, DB_Keys.USER_DB.value)


def load_db_data(db_filename: str) -> dict:
    with open(db_filename) as db:
        data = json.load(db)
    return data


def create_account(email: str, password: str):
    user_data = load_db_data(DB_Keys.USER_DB.value)
    login_data = load_db_data(DB_Keys.LOGIN_DB.value)
    new_user_id = random.randint(1, 1000)
    user_data[new_user_id] = {
        DB_Keys.PROFILE.value: {
            DB_Keys.FIRST_NAME.value: "",
            DB_Keys.LAST_NAME.value: "",
            DB_Keys.EMAIL.value: email,
        }
    }
    login_data[new_user_id] = {
        DB_Keys.EMAIL.value: email,
        DB_Keys.PASSWORD.value: password,
    }
    dump_data(user_data, DB_Keys.USER_DB.value)
    dump_data(login_data, DB_Keys.LOGIN_DB.value)


def dump_data(data: dict, db_filename: str):
    with open(db_filename, "w") as db:
        json.dump(data, db)
