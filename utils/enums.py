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
    PRIMARY_DARKER = "#B1DAC9"
    PRIMARY_LIGHTER = ft.colors.TEAL_ACCENT_100
    SECONDARY = "#EEEDD7"
    ACCENT = "#ffa500"
    WHITE = ft.colors.WHITE
    BLACK = ft.colors.BLACK
    ING = "#ff6201"
    MBANK = "#008520"
    APPLE_PAY = ft.colors.WHITE
    REVOLUT = ft.colors.WHITE
    SANTANDER = "#ec0000"
    PAYPAL = "#019cde"
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
