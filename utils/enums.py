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


class FinancingSrc(StrEnum):
    APPLE_PAY = "applepay"
    MBANK = "mbank"
    REVOLUT = "revolut"
    SANTANDER = "santander"
    PAYPAL = "paypal"
    ING = "ing"


def get_logo_src(source_name: str):
    match source_name.lower():
        case FinancingSrc.MBANK:
            return FinancingSrcPhotosURLs.MBANK
        case FinancingSrc.ING:
            return FinancingSrcPhotosURLs.ING
        case FinancingSrc.REVOLUT:
            return FinancingSrcPhotosURLs.REVOLUT
        case FinancingSrc.PAYPAL:
            return FinancingSrcPhotosURLs.PAYPAL
        case FinancingSrc.SANTANDER:
            return FinancingSrcPhotosURLs.SANTANDER
        case FinancingSrc.APPLE_PAY:
            return FinancingSrcPhotosURLs.APPLE_PAY
        case _:
            return String.EMPTY


def get_theme_color(source_name: str):
    match source_name.lower():
        case FinancingSrc.MBANK:
            return Colors.MBANK
        case FinancingSrc.ING:
            return Colors.ING
        case FinancingSrc.REVOLUT:
            return Colors.REVOLUT
        case FinancingSrc.PAYPAL:
            return Colors.PAYPAL
        case FinancingSrc.SANTANDER:
            return Colors.SANTANDER
        case FinancingSrc.APPLE_PAY:
            return Colors.APPLE_PAY
        case _:
            return String.EMPTY


class FinancingSrcPhotosURLs(StrEnum):
    APPLE_PAY = "https://lh3.googleusercontent.com/pw/AP1GczOCyddBGnewDifbL7irCXF1IUkAYWjpJNRNOKwQ_WFJiOmthp-h4IeiCT-MfzJ2cg9G-n51jAbkf6X-ptkeHc5TNNM8K6EgghtN8WGcW9MCC6bIvGfYJuk8jaYKz8wLjOxLFp6JoX1f7cx2y59yc2Q=w150-h150-s-no-gm"
    MBANK = "https://lh3.googleusercontent.com/pw/AP1GczMGmclVSSzuCUoWlVTmhjYvo42j1mI9LZ6hQDH3uwuD2na9Extl4EEnntFDn1a4DaWahK9trRvVKJqb2HFC9zq3lxQWiuumXufGH2NBO-7gwTpFXWwYqQofoYyBAdxKm1le5FOWXSInDhYa47dYjvY=w160-h160-s-no-gm"
    REVOLUT = "https://lh3.googleusercontent.com/pw/AP1GczO3xHEolUpxRVqhfpa3Aw2xFjG5s0ILBc3ui7kaWydz53nwpnipkJNjKMXFnSocEitxIVi5YhPUyxk5P2fawavPz-gX4HeVuO9Z9NwxfqBja8OhjkQktqCeO7YMRgFty76IDofVMriFXzyvptcIQQk=w160-h160-s-no-gm"
    SANTANDER = "https://lh3.googleusercontent.com/pw/AP1GczMgTKDgaFIH_9R5tCXLvM-8Jqg3tAbhymE0fL1K0s2AOhvceaLmdL7f-OuckyAr2y7eDUbhrmc5b1CWyO_ztxfOjwqYNY8K6VjXjpGb7CihezWKr8C3-WgJ33MHuFaP7YgOKwR_NFPQroev0WvKSSA=w160-h160-s-no-gm"
    PAYPAL = "https://lh3.googleusercontent.com/pw/AP1GczNOzTr0GdXO-W3k_TRwokN8MHnlPrf0VJkOEZAVhfqPOVCODIzHZ8irFHlrWstom5gqt2Ueu483ZR2lCgf0U_tm3u-4xXez8U5uE1wK77naoeFiE-owfCWR_SQ1OvZiEio5On6rx7t8FzhCXvE6rOc=w160-h160-s-no-gm"
    ING = "https://lh3.googleusercontent.com/pw/AP1GczOPgwLTS1Z4qBKqZ9MWSZZtDa6wV1XFZPp2mp1NwDTp4WYj4e0ejARbQfXLSTYresfgdhFGaIXLzvsz4ZjAwtK1UalZn4f_jByZKrFVZxfjujK5POfWqMG5llLlR5pjgPwZMDxnEGKRKrJEwJd8spc=w160-h160-s-no-gm"


class DateFormat(StrEnum):
    dmY = "%d-%m-%Y"
    Ymd = "%Y-%m-%d"
    mdY = "%m-%d-%Y"
    dmY_HHMM = "%d-%m-%Y %H:%M"
    Ymd_HHMM = "%Y-%m-%d %H:%M"
    mdY_HHMM = "%m-%d-%Y %H:%M"
    dmY_HHMMSS = "%d-%m-%Y %H:%M:%S"
    Ymd_HHMMSS = "%Y-%m-%d %H:%M:%S"
    mdY_HHMMSS = "%m-%d-%Y %H:%M:%S"
