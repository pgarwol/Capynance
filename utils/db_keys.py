from enum import Enum


class DB_Keys(Enum):
    ENCODING = "utf-8"
    LOGIN_DB = "login_database.json"
    USER_DB = "user_database.json"
    PROFILE = "profile"
    PASSWORD = "password"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    CALENDAR = "calendar"
    FINANCES = "finances"
    SOCIAL = "social"
    SETTINGS = "settings"
