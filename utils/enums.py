from enum import StrEnum
import flet as ft


class String(StrEnum):
    EMPTY = ""
    SPACE = " "


class DBFields(StrEnum):
    RELATIVE_DB_PATH = "./database/"
    BUILD_LOG_PATH = "./database/built_views.log"
    ENCODING = "utf-8"
    LOGIN_DB = "login_database.json"
    USER_DB = "users/"
    PROFILE = "profile"
    PASSWORD = "password"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    CALENDAR = "calendar"
    FINANCES = "finances"
    SOCIAL = "social"
    SETTINGS = "settings"
    STATS = "stats"
    MANUAL_SPENDING = "manual-spending"


class FletNames(StrEnum):
    APP_NAME = "Capynance."
    VIEW = "view"
    ROUTE = "route"
    PAGE = "page"
    CALENDAR = "calendar"
    FINANCES = "finances"
    HOME = "home"
    LOGIN = "login"
    REGISTER = "register"
    SCAN = "scan"
    SETTINGS = "settings"
    SHOP = "shop"
    SOCIAL = "social"
    STATS = "stats"
    PROFILE = "profile"


class Colors(StrEnum):
    # PRIMARY_DARKER = "#B1DAC9"  # light aquamarine
    PRIMARY_DARKER = "#2EC4B6"  # lght green
    PRIMARY_LIGHTER = "#CBF3F0"  # light aquamarine (but darker than primary_dark ?)
    SECONDARY = "#FFFFFF"  # light beige
    ACCENT = "#FF9F1C"  # light orange
    WHITE = ft.colors.WHITE
    BLACK = ft.colors.BLACK

    ING = "#ff6201"  # orange
    MBANK = "#008520"  # green
    APPLE_PAY = ft.colors.WHITE
    REVOLUT = ft.colors.WHITE
    SANTANDER = "#ec0000"  # red
    PAYPAL = "#019cde"  # blue
    POSITIVE = ft.colors.GREEN_500
    NEGATIVE = ft.colors.RED_500


class Currencies(StrEnum):
    POLISH_ZLOTY = "ZŁ"
    EURO = "EUR"
    US_DOLLAR = "USD"
    JAPANESE_YEN = "JPY"


class LanguageCodes(StrEnum):
    POLISH = "PL"
    ENGLISH = "EN"
    GERMAN = "DE"
    DUTCH = "NL"
    SPANISH = "ES"
