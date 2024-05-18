from enum import StrEnum
import flet as ft


class String(StrEnum):
    EMPTY = ""


class DBFields(StrEnum):
    RELATIVE_DB_PATH = "./database/"
    BUILD_LOG_PATH = "./database/built_views.log"
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


class Colors(StrEnum):
    PRIMARY_DARKER = "#B1DAC9"  # light aquamarine
    PRIMARY_LIGHTER = (
        ft.colors.TEAL_ACCENT_100
    )  # light aquamarine (but darker than primary_dark ?)
    SECONDARY = "#EEEDD7"  # light beige
    ACCENT = "#ffa500"  # light orange
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
