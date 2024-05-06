from enum import Enum


class User:
    def __init__(self, id: str, first_name: str, last_name: str, email: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # settings = Settings(language=Langs.PL)


class Statistics: ...


class Langs(Enum):
    PL = 0
    EN = 1
    DE = 2
    NL = 3


class Settings:
    language: Langs
