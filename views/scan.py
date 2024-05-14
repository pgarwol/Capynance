from views.view import View
from components.component import Component
from components.default_components import defaults
import flet as ft


scan = View(name="scan", route="/scan")
scan.add_component(defaults["STATISTICS_BAR"])
scan.add_component(
    Component([ft.Text("SKANOWANIE PARAGONU")], "View representing scanning QR codes.")
)
scan.add_component(defaults["NAVIGATION_BAR"])
print(scan)
