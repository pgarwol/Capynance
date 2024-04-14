from views.view import View
from components.component import Component
from components.default_components import default_components
from datetime import datetime
import flet as ft

calendar = View("/calendar")


def change_date(e):
    print(f"Date picker changed, value is ")


def date_picker_dismissed(e):
    print(f"Date picker dismissed, value is ")


calendar_component = Component(
    content=[
        ft.DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime(2023, 10, 1),
            last_date=datetime(2024, 10, 1),
        ),
        ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: print(),
        ),
    ]
)
calendar.add_component(default_components["STATS"])
calendar.add_component(calendar_component)
calendar.add_component(default_components["NAVIGATION"])
