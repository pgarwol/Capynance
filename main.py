import utils.services as services
from session import Session
from views.shop import shop
from views.home import home
from views.scan import scan
from views.login import login
from views.social import social
from utils.enums import DBFields, FLET_NAMES
from views.register import register
from views.calendar import calendar
from views.finances import finances
from views.settings import settings
from views.calendar import calendar
from components.default_components import defaults
from utils.lang import Lang
import flet as ft

all_views = (shop, home, scan, login, register, social, calendar, finances, settings)


class App:
    name = "Capynance."
    session = None

    navigation_bar_items = {
        0: {FLET_NAMES.VIEW: scan, FLET_NAMES.ROUTE: scan.route},
        1: {FLET_NAMES.VIEW: shop, FLET_NAMES.ROUTE: shop.route},
        2: {FLET_NAMES.VIEW: calendar, FLET_NAMES.ROUTE: calendar.route},
        3: {FLET_NAMES.VIEW: home, FLET_NAMES.ROUTE: home.route},
        4: {FLET_NAMES.VIEW: finances, FLET_NAMES.ROUTE: finances.route},
        5: {FLET_NAMES.VIEW: social, FLET_NAMES.ROUTE: social.route},
        6: {FLET_NAMES.VIEW: settings, FLET_NAMES.ROUTE: settings.route},
        7: {FLET_NAMES.VIEW: login, FLET_NAMES.ROUTE: login.route},
        8: {FLET_NAMES.VIEW: register, FLET_NAMES.ROUTE: register.route},
    }

    def main(self, page: ft.Page) -> None:
        def attach_pages() -> None:
            for view in all_views:
                view.attach_page(page)

        def on_init() -> None:
            attach_pages()

            defaults["NAVIGATION_BAR"].content[0].content.on_change = lambda e: page.go(
                route=self.navigation_bar_items[e.control.selected_index][
                    FLET_NAMES.ROUTE
                ]
            )
            defaults["STATISTICS_BAR"].content[0].actions[
                0
            ].on_click = lambda _: page.update()

        page.title = self.name

        on_init()

        def route_change(route: str) -> None:
            page.views.clear()
            page.views.append(
                self.navigation_bar_items[get_view_index(route=home.route)][
                    FLET_NAMES.VIEW
                ].build()
            )
            if page.route != home.route:
                page.views.append(
                    self.navigation_bar_items[get_view_index(route=page.route)][
                        FLET_NAMES.VIEW
                    ].build()
                )

            page.update()

        def view_pop(view: ft.View):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        def get_view_index(route: str) -> int | None:
            return next(
                (
                    key
                    for key in self.navigation_bar_items.keys()
                    if self.navigation_bar_items[key][FLET_NAMES.ROUTE] == route
                ),
                None,
            )

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)


if __name__ == "__main__":
    app = App()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)
