from services import read_user_from_db
from abc import ABC, abstractmethod


class Session:
    def __init__(self, user_id: str | int, language: str):
        self.logged_user = read_user_from_db(id=str(user_id))
        self.language = language


# Initialized after login
# Terminated after log out
# @TODO: Settings mechanics: dark mode, lang etc.
