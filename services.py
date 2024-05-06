from user import User
import json


def read_user_from_db(id: int) -> User:
    with open("database.json") as db:
        user_data = json.load(db)[str(id)]

    # user = User(
    #     id=id,
    #     first_name=user_data["profile"]["first_name"],
    # )


def save_entity() -> None: ...
