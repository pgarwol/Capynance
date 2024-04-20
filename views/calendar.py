from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


calendar = View(name="calendar", route="/calendar")
calendar.add_component(defaults["STATISTICS_BAR"])
calendar.add_component(Component([ft.Text("KALENDARZ")], "View representing calendar."))
calendar.add_component(defaults["NAVIGATION_BAR"])
print(calendar)
