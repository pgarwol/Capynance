from views.view import View
from services import create_account
from components.component import Component
from components.default_components import defaults
from utils.colors import Color
from views.home import home
import re
import flet as ft
from typing import Tuple
from utils.styles import Style

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
}


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def do_register(email: str, password: str, password_confirmation: str):
    if email is None or password is None or password_confirmation is None:
        return
    if validate_email(email):
        print("All good")
        if password == password_confirmation:
            create_account(email, password)
            register.var["page"].go(home.route)
        else:
            print("Passwords must be the same.")
    else:
        print("Email is not correct")
