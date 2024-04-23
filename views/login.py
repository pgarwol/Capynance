from components.component import Component
from views.view import View
from typing import Tuple
import flet as ft

login = View(name="Login", route="/")

login.add_component(
    Component(
        content=[
            ft.TextField(
                label="Login",
                border=None,
                border_width=0,
                filled=True,
                cursor_color=ft.colors.RED_600,
                label_style=ft.TextStyle(
                    color=ft.colors.RED_600, weight=ft.FontWeight.W_400
                ),
            ),
            ft.TextField(
                label="Password ",
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
                text="Submit",
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED_500,
            ),
        ],
        description="Login page.",
    )
)


def initialize_login_fields() -> Tuple[ft.TextField, ft.TextField]:
    login_input = login.components[0].content[0]
    password_input = login.components[0].content[1]

    return login_input, password_input
