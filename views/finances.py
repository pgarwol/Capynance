from views.view import View
from utils.enums import FletNames
from components.component import Component, DefaultComponents
import flet as ft


finances = View(name=FletNames.FINANCES, route=f"/{FletNames.FINANCES}")
finances.add_component(DefaultComponents.STATISTICS_BAR.value)
finances.add_component(
    Component([ft.Text("FINANSE")], "View representing finance management.")
)
finances.add_component(DefaultComponents.NAVIGATION_BAR.value)
print(finances)
