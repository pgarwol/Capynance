from views.view import View
from components.component import Component
import flet as ft
from typing import Tuple

login = View(name="Login", route="/")

login.add_component(
    Component(
        content=[
            ft.SafeArea(
                ft.Image(
                    src="https://img.freepik.com/free-vector/forest-scene-with-wild-animals_1308-114385.jpg?w=1380&t=st=1715025124~exp=1715025724~hmac=2029704265bfa5fb3d7d035ec399ec793f14c925e4e2a7711e10a0b79a3dc6cd",
                    width=250,
                    height=250,
                    fit=ft.ImageFit.COVER,
                    error_content=ft.Text("Image error."),
                ),
            ),
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
            ft.ElevatedButton(
                text="Zaloguj",
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED_500,
            ),
            ft.TextButton(text="Nie masz jeszcze konta? Zarejestruj się!"),
        ],
        description="Login page.",
    )
)


def initialize_login_fields() -> Tuple[ft.TextField, ft.TextField]:
    email_input = login.components[0].content[1]
    password_input = login.components[0].content[2]

    return email_input, password_input
