import services
from ft_keys import FT_Keys
from session import Session
from views.shop import shop
from views.home import home
from views.scan import scan
from views.login import login
from views.register import (
    register,
    do_register,
    validate_email,
    create_account,
    initialize_register_fields,
)
from views.social import social
from views.calendar import calendar
from views.finances import finances
from views.settings import settings
from views.calendar import calendar
from components.component import Component
from views.login import initialize_login_fields
from components.default_components import defaults
import flet as ft


class App:
    name = "Capynance."

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
        def on_init() -> None:
            defaults["NAVIGATION_BAR"].content[0].content.on_change = lambda e: page.go(
                route=self.navigation_bar_items[e.control.selected_index][
                    FT_Keys.ROUTE.value
                ]
            )

            login_email_input, login_password_input = initialize_login_fields()
            login.get_component(0).content[-2].on_click = lambda _: log_user_in(
                login_email_input.value, login_password_input.value
            )
            login.get_component(0).content[-1].on_click = lambda _: page.go(
                register.route
            )

            (
                register_email_input,
                register_password_input,
                register_confirm_pwd_input,
            ) = initialize_register_fields()

            register.get_component(0).content[-2].on_click = lambda _: page.go(
                login.route
            )
            register.get_component(0).content[-1].on_click = lambda _: do_register(
                register_email_input.value,
                register_password_input.value,
                register_confirm_pwd_input.value,
            )

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

        def log_user_in(email: str | None, password: str | None):
            if email is None or password is None:
                return

            logged_in_successfully, user_id = services.is_login_valid(email, password)
            if logged_in_successfully:
                self.session = Session(user_id)
                print(self.session.logged_user)
                page.go(home.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)


if __name__ == "__main__":
    app = App()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)
