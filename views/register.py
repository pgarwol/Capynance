from views.home import home
from views.view import View
from utils.styles import Style
from services import create_account
from components.component import Component
import re
import flet as ft

register = View(name="Register", route="/register")
register.add_component(
    Component(
        content=[
            ft.TextField(label="e-mail", **Style.TextField.value),
            ft.TextField(
                label="hasło",
                password=True,
                can_reveal_password=True,
                **Style.TextField.value
            ),
            ft.TextField(
                label="powtórz hasło",
                password=True,
                can_reveal_password=True,
                **Style.TextField.value
            ),
            ft.Text(),
            # TODO: Incorrect data info,
            ft.TextButton(
                text="Masz już konto? Zaloguj się!",
                on_click=lambda _: register.var["page"].go("/"),
            ),
            ft.ElevatedButton(
                text="Zarejestruj",
                on_click=lambda _: do_register(
                    register.var["email"].value,
                    register.var["password"].value,
                    register.var["password_confirmation"].value,
                ),
                **Style.ElevatedButton.value
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
        register.var["page"].update()
        return

    if validate_email(email):
        if password == password_confirmation:
            create_account(email, password)
            register.var["page"].go(home.route)
        else:
            register.var["errors_output"].value = "Hasła muszą być takie same"
            register.var["page"].update()
    else:
        register.var["errors_output"].value = "Wszystkie pola muszą zostać wypełnione"
        register.var["page"].update()
