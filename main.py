from views.shop import shop
from views.calendar import calendar
from views.home import home
from views.finances import finances
from views.scan import scan
from views.settings import settings
from views.social import social
from views.calendar import calendar
from views.login import login
from views.login import initialize_login_fields
from components.component import Component
from components.default_components import defaults
import flet as ft


class App:
    name = "Capynance."

    navigation_bar_items = {
        0: {"view": scan, "route": scan.route},
        1: {"view": shop, "route": shop.route},
        2: {"view": calendar, "route": calendar.route},
        3: {"view": home, "route": home.route},
        4: {"view": finances, "route": finances.route},
        5: {"view": social, "route": social.route},
        6: {"view": settings, "route": settings.route},
        7: {"view": login, "route": login.route},
    }

    def main(self, page: ft.Page) -> None:
        page.title = self.name

        # Avoids page variable scope problem
        defaults["NAVIGATION_BAR"].content[0].content.on_change = lambda e: page.go(
            route=self.navigation_bar_items[e.control.selected_index]["route"]
        )
        login_input, password_input = initialize_login_fields()
        login.get_component(0).content[-1].on_click = lambda _: log_user_in(
            login_input.value, password_input.value
        )

        def route_change(route: str) -> None:
            page.views.clear()
            page.views.append(
                self.navigation_bar_items[get_view_index(route="/home")]["view"].build()
            )
            if page.route != "/home":
                page.views.append(
                    self.navigation_bar_items[get_view_index(route=page.route)][
                        "view"
                    ].build()
                )

            page.update()

        def view_pop(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        def get_view_index(route: str) -> int | None:
            return next(
                (
                    key
                    for key in self.navigation_bar_items.keys()
                    if self.navigation_bar_items[key]["route"] == route
                ),
                None,
            )

        def log_user_in(login: str | None, password: str | None):
            if login is None or password is None:
                return

            # @TODO: Legit login system
            if login == "admin" and password == "admin":
                page.go("/home")

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)


if __name__ == "__main__":
    app = App()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)
