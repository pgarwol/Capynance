from dataclasses import dataclass
from enum import Enum


@dataclass
class User:
    def __init__(self, id, first_name, last_name, language):
        # read_properties_from_db()
        profile = Profile(first_name=first_name, last_name=last_name)
        settings = Settings(language=Langs.PL)


@dataclass
class Profile:
    first_name: str
    last_name: str


@dataclass
class Statistics: ...


class Langs(Enum):
    PL = 0
    EN = 1
    DE = 2
    NL = 3


@dataclass
class Settings:
    language: Langs
