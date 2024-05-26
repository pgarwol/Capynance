from views import init_settings
from views.home import home, init_home
from views.view import View
from utils.enums import Colors, FletNames, String
from utils.styles import Style
import utils.services as services
from views.register import register
from session import Session
from views.calendar import init_calendar
from views.finances import init_finances
from views.scan import init_scan
from components.component import Component
from components.component import DefaultComponents, init_stats
from page import Page
from typing import Tuple
import flet as ft

login = View(name=FletNames.LOGIN, route="/")
login.add_component(
    Component(
        content=[
            ft.SafeArea(
                ft.Image(
                    src="https://lh3.googleusercontent.com/pw/AP1GczM8ZzSJnB2PxA1RqdI04DnJf16ps6PE8-8Ppsy0Gt-xMairJPaW9h-oQJ5huSbJzlyD0d0L0RixI0EJmssHgf8KEJgI6B5jq9OW1W4zMzj8csIsfUwy5pmILFuQ0mLxZhX61uw7Pg6CnuhekOLDF0Y=w894-h894-s-no-gm?authuser=0",
                    width=250,
                    height=250,
                    fit=ft.ImageFit.COVER,
                    error_content=ft.Text("Image error."),
                ),
            ),
            email_textfield := ft.TextField(**Style.TextField.value),
            password_textfield := ft.TextField(
                password=True,
                can_reveal_password=True,
                **Style.TextField.value,
            ),
            log_in_button := ft.ElevatedButton(
                color=Colors.BLACK.value,
                bgcolor=Colors.ACCENT.value,
                on_click=lambda _: log_user_in(
                    login.var["email"].value, login.var["password"].value
                ),
            ),
            no_account_button := ft.TextButton(
                on_click=lambda _: Page.go(register.route),
            ),
        ],
        description="Login page.",
    )
)
login.var = {
    "email": login.components[0].content[1],
    "password": login.components[0].content[2],
}


def log_user_in(email: str | None, password: str | None):
    """
    Log a user into the system.

    Logs a user into the system if the provided email and password are valid.
    Sets the logged user's language, updates views with the new language,
    initializes the calendar, and redirects to the home page upon successful login.

    Args:
        email (str | None): The email of the user trying to log in.
        password (str | None): The password of the user trying to log in.

    Returns:
        None

    Raises:
        None
    """
    if email is None or password is None:
        return

    logged_in_successfully, user_id = services.is_login_valid(email, password)
    if logged_in_successfully:
        Session.set_logged_user(services.read_user_from_db(user_id))
        if "language" not in Session.get_logged_user().settings:
            Session.set_language("pl")
            print('Language not found in settings. Setting to "polish".')
        else:
            Session.set_language(Session.get_logged_user().settings["language"])
        Session.set_views(View.instances)
        login.var["email"].value = String.EMPTY
        login.var["password"].value = String.EMPTY
        Session.translate_views_content()
        init_calendar()
        init_finances()
        init_stats()
        init_scan()
        init_home()
        init_settings(email)
        Page.go(home.route)


def refresh_labels() -> None:
    email_textfield.label = login.lang["email"]
    password_textfield.label = login.lang["password"]
    log_in_button.text = login.lang["log_in"]
    no_account_button.text = login.lang["no_account"]


refresh_labels()

login.refresh_language_contents = refresh_labels


login.log()
