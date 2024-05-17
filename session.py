from utils.services import read_user_from_db
from abc import ABC, abstractmethod


class Session:

    @classmethod
    def set_logged_user(cls, logged_user):
        cls.logged_user = logged_user

    @classmethod
    def get_logged_user(cls):
        return cls.logged_user

    @classmethod
    def set_language(cls, language):
        cls.language = language

    @classmethod
    def get_language(cls):
        return cls.language


# Initialized after login
# Terminated after log out
# @TODO: Settings mechanics: dark mode, lang etc.
