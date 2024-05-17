import utils.services as services
from session import Session
from views.shop import shop
from views.home import home
from views.scan import scan
from views.login import login
from views.social import social
from utils.ft_keys import FT_Keys
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
        0: {FT_Keys.VIEW.value: scan, FT_Keys.ROUTE.value: scan.route},
        1: {FT_Keys.VIEW.value: shop, FT_Keys.ROUTE.value: shop.route},
        2: {FT_Keys.VIEW.value: calendar, FT_Keys.ROUTE.value: calendar.route},
        3: {FT_Keys.VIEW.value: home, FT_Keys.ROUTE.value: home.route},
        4: {FT_Keys.VIEW.value: finances, FT_Keys.ROUTE.value: finances.route},
        5: {FT_Keys.VIEW.value: social, FT_Keys.ROUTE.value: social.route},
        6: {FT_Keys.VIEW.value: settings, FT_Keys.ROUTE.value: settings.route},
        7: {FT_Keys.VIEW.value: login, FT_Keys.ROUTE.value: login.route},
        8: {FT_Keys.VIEW.value: register, FT_Keys.ROUTE.value: register.route},
    }

    def main(self, page: ft.Page) -> None:
        def attach_pages() -> None:
            for view in all_views:
                view.attach_page(page)

        def on_init() -> None:
            attach_pages()

            defaults["NAVIGATION_BAR"].content[0].content.on_change = lambda e: page.go(
                route=self.navigation_bar_items[e.control.selected_index][
                    FT_Keys.ROUTE.value
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
                    FT_Keys.VIEW.value
                ].build()
            )
            if page.route != home.route:
                page.views.append(
                    self.navigation_bar_items[get_view_index(route=page.route)][
                        FT_Keys.VIEW.value
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
                    if self.navigation_bar_items[key][FT_Keys.ROUTE.value] == route
                ),
                None,
            )

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)


if __name__ == "__main__":
    app = App()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)
