from views.view import View
from components.component import Component
from components.default_components import defaults
import flet as ft


finances = View(name="finances", route="/finances")
finances.add_component(defaults["STATISTICS_BAR"])
finances.add_component(
    Component([ft.Text("FINANSE")], "View representing finance management.")
)
finances.add_component(defaults["NAVIGATION_BAR"])
print(finances)
