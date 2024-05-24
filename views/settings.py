from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents
from utils.enums import FletNames, Colors
import flet as ft


settings = View(name=FletNames.SETTINGS, route=f"/{FletNames.SETTINGS}")
settings.add_component(
    Component(
        content=[
            ft.AppBar(
                title=ft.Text("Ustawienia aplikacji"),
                bgcolor=Colors.PRIMARY_DARKER
            )
        ],
        description="App bar showing the title of the page and allowing to navigate back to the home page.")
)
ViewsInitialStates.set_settings_copy(settings)
settings.log()
