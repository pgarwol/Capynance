from utils.db_keys import DB_Keys
import services
from enum import Enum


class User:
    def __init__(
        self,
        id: str,
        profile: dict,
        calendar: dict,
        finances: dict,
        social: dict,
        settings: dict,
    ):
        self.id = id
        self.profile = profile
        self.calendar = calendar
        self.finances = finances
        self.social = social
        self.settings = settings

        # settings = Settings(language=Langs.PL)

    def serialize(self):
        """
        Serializes the user data into a dictionary format.

        Returns:
            dict: The serialized user data.
        """
        return {DB_Keys.PROFILE.value: self.profile}

    def __repr__(self):
        return f"User(id = {self.id}, first_name = {self.profile[DB_Keys.FIRST_NAME.value]}, last_name = {self.profile[DB_Keys.LAST_NAME.value]}, email = {self.profile[DB_Keys.EMAIL.value]})"


class Statistics: ...


class Langs(Enum):
    PL = 0
    EN = 1
    DE = 2
    NL = 3


class Settings:
    language: Langs
