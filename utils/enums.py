from enum import StrEnum
import flet as ft


class String(StrEnum):
    EMPTY = ""


class DBFields(StrEnum):
    RELATIVE_DB_PATH = "./database/"
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


class FletNames(StrEnum):
    VIEW = "view"
    ROUTE = "route"
    CALENDAR = "calendar"
    FINANCES = "finances"
    HOME = "home"
    LOGIN = "login"
    REGISTER = "register"
    SCAN = "scan"
    SETTINGS = "settings"
    SHOP = "shop"
    SOCIAL = "social"


class Colors(StrEnum):
    PRIMARY_DARKER = "#B1DAC9"
    PRIMARY_LIGHTER = ft.colors.TEAL_ACCENT_100
    SECONDARY = "#EEEDD7"
    ACCENT = "#ECDB5E"
    WHITE = ft.colors.WHITE
    BLACK = ft.colors.BLACK
