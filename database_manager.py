import json

with open("database.json") as db:
    data = json.load(db)


def valid_login(login: str, password: str) -> bool:
    for user in data.keys():
        user_login = data[user]["login"]
        user_password = data[user]["password"]

        if user_login == login and user_password == password:
            return True

    return False
