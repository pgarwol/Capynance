import logging

from utils.sync_manager import SyncManager
from utils.theme_manager import ThemeManager
from views import init_settings
from views.home import home, init_home
from views.view import View
from utils.enums import Colors, FletNames, String, DBFields
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


class LocalThemeManager:
    """
    A class used to represent a Local Theme Manager. It helps to manage the theme of the application.
    """

    def __init__(self, theme: ft.ThemeMode):
        """
        Initializes the LocalThemeManager with the provided theme.

        Args:
            theme (ft.ThemeMode): The theme to be remembered.

        Returns:
            None
        """
        self.theme_mode = theme

    def on_change_theme(self, theme: ft.ThemeMode) -> None:
        """
        Sets the session dark mode value when the theme changes. It is set to True if the theme is DARK,
        False otherwise.
        :param theme: The current theme of the application.
        :return: None
        """
        self.theme_mode = theme
        Session.get_logged_user().settings["dark_mode"] = True if theme == ft.ThemeMode.DARK else False
        SyncManager.sync_settings()


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

        # Set language based on user settings.
        current_user_settings = Session.get_logged_user().settings
        if "language" not in current_user_settings:
            Session.set_language("pl")
            logging.warning('Language not found in settings. Setting to "polish".')
        else:
            Session.set_language(current_user_settings["language"])

        Session.set_views(View.instances)
        login.var["email"].value = String.EMPTY
        login.var["password"].value = String.EMPTY
        # Session controls the language of the app.
        Session.translate_views_content()

        # Set theme based on user settings.
        if "dark_mode" not in current_user_settings:
            current_user_settings["dark_mode"] = False
            logging.warning('Theme preference not found in settings. Setting to default "light".')
        # ThemeManager controls the theme of the app.
        ThemeManager.toggle_dark_mode(current_user_settings['dark_mode'])
        # Create a LocalThemeManager instance with the current theme mode
        theme_info = LocalThemeManager(ThemeManager.theme_mode)
        # Add the LocalThemeManager instance as an observer to the ThemeManager
        ThemeManager.add_observer(theme_info)

        init_calendar()
        init_finances()
        init_stats()
        init_scan()
        init_home()
        init_settings(email, current_user_settings['dark_mode'])
        SyncManager.set_init_functions(init_calendar=init_calendar, init_finances=init_finances, init_stats=init_stats,
                                       init_scan=init_scan, init_home=init_home)
        SyncManager.set_db_fields(DBFields)
        Page.go(home.route)


def refresh_labels() -> None:
    email_textfield.label = login.lang["email"]
    password_textfield.label = login.lang["password"]
    log_in_button.text = login.lang["log_in"]
    no_account_button.text = login.lang["no_account"]


refresh_labels()

login.refresh_language_contents = refresh_labels

login.log()
