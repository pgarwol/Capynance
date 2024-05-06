from enum import Enum
from db_keys import DB_Keys


class User:
    def __init__(self, id: str, first_name: str, last_name: str, email: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # settings = Settings(language=Langs.PL)

    def serialize(self):
        return {
            DB_Keys.PROFILE.value: {
                DB_Keys.FIRST_NAME.value: self.first_name,
                DB_Keys.LAST_NAME.value: self.first_name,
                DB_Keys.EMAIL.value: self.email,
            }
        }

    def __repr__(self):
        return f"User(id = {self.id}, first_name = {self.first_name}, last_name = {self.last_name}, email = {self.email})"


class Statistics: ...


class Langs(Enum):
    PL = 0
    EN = 1
    DE = 2
    NL = 3


class Settings:
    language: Langs
