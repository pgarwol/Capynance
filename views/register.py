from views.home import home
from views.view import View
from utils.styles import Style
from utils.enums import FletNames
import utils.services as services
from components.component import Component
from page import Page
import re
import flet as ft

register = View(name=FletNames.REGISTER, route=f"/{FletNames.REGISTER}")
register.add_component(
    Component(
        content=[
            email_textfield := ft.TextField(label=None, **Style.TextField.value),
            password_textfield := ft.TextField(
                label=None,
                password=True,
                can_reveal_password=True,
                **Style.TextField.value,
            ),
            confirm_password_textfield := ft.TextField(
                label=None,
                password=True,
                can_reveal_password=True,
                **Style.TextField.value,
            ),
            ft.Text(),
            # TODO: Incorrect data info,
            has_account_button := ft.TextButton(
                text=register.lang["has_account"],
                on_click=lambda _: Page.go("/"),
            ),
            register_button := ft.ElevatedButton(
                text=None,
                on_click=lambda _: do_register(
                    register.var["email"].value,
                    register.var["password"].value,
                    register.var["password_confirmation"].value,
                ),
                **Style.ElevatedButton.value,
            ),
        ],
        description="View used for user registration",
    )
)
register.var = {
    "email": register.components[0].content[0],
    "password": register.components[0].content[1],
    "password_confirmation": register.components[0].content[2],
    "errors_output": register.components[0].content[3],
}


def validate_email(email: str) -> bool:
    """
    Validates the format of an email address.

    Args:
        email (str): The email address to be validated.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def do_register(email: str, password: str, password_confirmation: str) -> None:
    # TODO: data validation
    """
    Registers a user with the provided email and password.

    Args:
        email (str): The email of the user.
        password (str): The password for the user account.
        password_confirmation (str): The confirmation of the password.

    Returns:
        None
    """
    if email is None or password is None or password_confirmation is None:
        register.var["errors_output"].value = "Wszystkie pola muszą zostać wypełnione"
        Page.update()
        return

    if validate_email(email):
        if password == password_confirmation:
            services.create_account(email, password)
            Page.go(home.route)
        else:
            register.var["errors_output"].value = "Hasła muszą być takie same"
            Page.update()
    else:
        register.var["errors_output"].value = "Wszystkie pola muszą zostać wypełnione"
        Page.update()


def refresh_labels() -> None:
    email_textfield.label = register.lang["email"]
    password_textfield.label = register.lang["password"]
    confirm_password_textfield.label = register.lang["confirm_password"]
    has_account_button.text = register.lang["has_account"]
    register_button.text = register.lang["register"]


refresh_labels()

register.refresh_language_labels = refresh_labels

register.log()
