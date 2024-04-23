from components.component import Component
from views.view import View
import flet as ft

login = View(name="Login", route="/login")

login.add_component(
    Component(
        content=[
            login_input := ft.TextField(
                label="Login",
                border=None,
                border_width=0,
                filled=True,
                cursor_color=ft.colors.RED_600,
                label_style=ft.TextStyle(
                    color=ft.colors.RED_600, weight=ft.FontWeight.W_400
                ),
            ),
            password_input := ft.TextField(
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
                on_click=lambda _: (
                    print("UDANE LOGOWANIE")
                    if login_input.value == "admin" and password_input.value == "admin"
                    else print("NIEUDANE LOGOWANIE")
                ),
            ),
        ],
        description="Login page.",
    )
)
print(login)
