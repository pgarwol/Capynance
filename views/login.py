from views.view import View
from components.component import Component
import flet as ft
from typing import Tuple
from session import Session
from views.home import home
from views.register import register
from utils.colors import Color
from utils.styles import Style
import services

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
            ft.TextField(label="e-mail", **Style.TextField.value),
            ft.TextField(
                label="hasło",
                password=True,
                can_reveal_password=True,
                **Style.TextField.value
            ),
            ft.ElevatedButton(
                text="Zaloguj",
                color=Color.BLACK.value,
                bgcolor=Color.ACCENT.value,
                on_click=lambda _: log_user_in(
                    login.var["email"].value, login.var["password"].value
                ),
            ),
            ft.TextButton(
                text="Nie masz jeszcze konta? Zarejestruj się!",
                on_click=lambda _: login.var["page"].go(register.route),
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
    if email is None or password is None:
        return

    logged_in_successfully, user_id = services.is_login_valid(email, password)
    if logged_in_successfully:
        session = Session(user_id, language="pl")
        print(session.logged_user)
        login.var["page"].go(home.route)
