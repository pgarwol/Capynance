from views.view import View
import utils.services as services
from components.component import Component, DefaultComponents
from utils.enums import FletNames
import flet as ft


settings = View(name=FletNames.SETTINGS, route=f"/{FletNames.SETTINGS}")
settings.add_component(DefaultComponents.STATISTICS_BAR.value)
settings.add_component(
    Component([ft.Text("USTAWIENIA")], "View representing Settings.")
)
settings.add_component(DefaultComponents.NAVIGATION_BAR.value)
settings.log()
