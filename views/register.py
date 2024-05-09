from views.view import View
from services import create_account
from components.component import Component
from components.default_components import defaults
import re
import flet as ft
from typing import Tuple

register = View(name="Register", route="/register")
register.add_component(
    Component(
        content=[
            ft.TextField(
                label="e-mail",
                border=None,
                border_width=0,
                filled=True,
                cursor_color=ft.colors.RED_600,
                label_style=ft.TextStyle(
                    color=ft.colors.RED_600, weight=ft.FontWeight.W_400
                ),
            ),
            ft.TextField(
                label="hasło",
                password=True,
                can_reveal_password=True,
                border=None,
                border_width=0,
                filled=True,
                cursor_color=ft.colors.RED_600,
                label_style=ft.TextStyle(
                    color=ft.colors.RED_600, weight=ft.FontWeight.W_400
                ),
            ),
            ft.TextField(
                label="powtórz hasło",
                password=True,
                can_reveal_password=True,
                border=None,
                border_width=0,
                filled=True,
                cursor_color=ft.colors.RED_600,
                label_style=ft.TextStyle(
                    color=ft.colors.RED_600, weight=ft.FontWeight.W_400
                ),
            ),
            ft.Text(),
            # TODO: Incorrect data info
            ft.ElevatedButton(
                text="Zarejestruj",
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED_500,
            ),
        ],
        description="View used for user registration",
    )
)


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
        else:
            print("Passwords must be the same.")
    else:
        print("Email is not correct")


def initialize_register_fields() -> Tuple[
    ft.TextField,
    ft.TextField,
    ft.TextField,
]:
    email_input = register.components[0].content[0]
    password_input = register.components[0].content[1]
    confirm_password_input = register.components[0].content[2]

    return email_input, password_input, confirm_password_input
