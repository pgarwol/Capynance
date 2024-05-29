import signal
import sys

import flet as ft
from flet_core import theme

import utils.services as services
from components.component import DefaultComponents
from page import Page
from utils.enums import FletNames, Colors
from utils.theme_manager import ThemeManager
from views.calendar import calendar, reset_calendar
from views.finances import finances, reset_finances
from views.home import home
from views.login import login
from views.register import register
from views.scan import scan
from views.settings import settings
from views.shop import shop
from views.view import View


class App:
    name = FletNames.APP_NAME
    session = None

    navigation_bar_items = {
        0: {FletNames.VIEW: scan, FletNames.ROUTE: scan.route},
        1: {FletNames.VIEW: shop, FletNames.ROUTE: shop.route},
        2: {FletNames.VIEW: home, FletNames.ROUTE: home.route},
        3: {FletNames.VIEW: calendar, FletNames.ROUTE: calendar.route},
        4: {FletNames.VIEW: finances, FletNames.ROUTE: finances.route},
        5: {FletNames.VIEW: login, FletNames.ROUTE: login.route},
        6: {FletNames.VIEW: register, FletNames.ROUTE: register.route},
        7: {FletNames.VIEW: settings, FletNames.ROUTE: settings.route},
    }

    def main(self, page: ft.Page) -> None:
        page.fonts = {
            "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf",
            "ConcertOne": "https://github.com/M4agicBean/Capynance-fonts/blob/main/ConcertOne-Regular.ttf?raw=true",
            "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
            "RubikMonoOne": "https://github.com/M4agicBean/Capynance-fonts/blob/main/RubikMonoOne-Regular.ttf?raw=true",
        }
        Page.set_page(page=page)
        # page.vertical_alignment = ft.MainAxisAlignment.CENTER
        # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def on_init() -> None:
            DefaultComponents.NAVIGATION_BAR.value.content[0].content.on_change = (
                lambda e: Page.go(
                    route=self.navigation_bar_items[e.control.selected_index][
                        FletNames.ROUTE
                    ]
                )
            )
            DefaultComponents.STATISTICS_BAR.value.content[0].actions[
                0
            ].on_click = lambda _: save_and_flush()

        page.title = self.name

        on_init()

        def route_change(route: str) -> None:
            page.views.clear()
            page.views.append(
                self.navigation_bar_items[get_view_index(route=home.route)][
                    FletNames.VIEW
                ].build()
            )
            if page.route != home.route:
                page.views.append(
                    self.navigation_bar_items[get_view_index(route=page.route)][
                        FletNames.VIEW
                    ].build()
                )

            Page.update()

        def view_pop(view: ft.View):
            page.views.pop()
            top_view = page.views[-1]
            Page.go(top_view.route)

        def get_view_index(route: str) -> int | None:
            return next(
                (
                    key
                    for key in self.navigation_bar_items.keys()
                    if self.navigation_bar_items[key][FletNames.ROUTE] == route
                ),
                None,
            )

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        Page.go(page.route)

        # Theming
        page.theme = theme.Theme(color_scheme_seed=Colors.PRIMARY_DARKER)
        ThemeManager.toggle_dark_mode(toggle_on=False)


def save_and_flush() -> None:
    DefaultComponents.NAVIGATION_BAR.value.content[0].selected_index = (
        DefaultComponents.DEFAULT_MENU_SELECTION.value
    )
    View.reset_views()
    reset_calendar()
    reset_finances()
    Page.update()


def cleanup(signum=None, frame=None):
    services.flush_build_log()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    try:
        app = App()
        ft.app(target=app.main)
    finally:
        cleanup()
