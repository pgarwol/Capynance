from views.view import View
from components.component import Component, DefaultComponents
from utils.enums import FletNames
import flet as ft


scan = View(name=FletNames.SCAN, route=f"/{FletNames.SCAN}")
scan.add_component(DefaultComponents.STATISTICS_BAR.value)
scan.add_component(
    Component(
        [ft.Text("SKANOWANIE PARAGONU")],
        description="View representing scanning QR codes.",
    )
)
scan.add_component(DefaultComponents.NAVIGATION_BAR.value)
print(scan)
