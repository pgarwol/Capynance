from enum import Enum
from views.shop import shop
from views.home import home
from views.scan import scan
from views.login import login
from views.login import login
from views.social import social
from views.register import register
from views.calendar import calendar
from views.finances import finances
from views.settings import settings
from views.calendar import calendar


class FT_Keys(Enum):
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
    ALL_VIEWS_NAMES = (
        CALENDAR,
        FINANCES,
        HOME,
        LOGIN,
        REGISTER,
        SCAN,
        SETTINGS,
        SHOP,
        SOCIAL,
    )
