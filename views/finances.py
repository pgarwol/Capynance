from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


finances = View(name="finances", route="/finances")
finances.add_component(defaults["STATISTICS_BAR"])
finances.add_component(
    Component([ft.Text("FINANSE")], "View representing finance management.")
)
finances.add_component(defaults["NAVIGATION_BAR"])
print(finances)
