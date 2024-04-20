from views.shop import shop
from views.calendar import calendar
from views.home import home
from views.finances import finances
from views.scan import scan
from views.settings import settings
from views.social import social
from views.calendar import calendar
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
    }

    def main(self, page: ft.Page) -> None:
        page.title = self.name

        # Avoids page variable scope problem
        defaults["NAVIGATION_BAR"].content[0].content.on_change = lambda e: page.go(
            route=self.navigation_bar_items[e.control.selected_index]["route"]
        )

        def route_change(route: str) -> None:
            page.views.clear()
            page.views.append(
                self.navigation_bar_items[get_view_index(route="/")]["view"].build()
            )
            if page.route != "/":
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

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)


if __name__ == "__main__":
    app = App()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)
