from components.default_components import defaults
from components.component import Component
from views.view import View
import datetime
import flet as ft


def change_date(e):
    print(f"Date picker changed, value is {date_picker.value}")


def date_picker_dismissed(e):
    print(f"Date picker dismissed, value is {date_picker.value}")


calendar = View(name="calendar", route="/calendar")
calendar.add_component(defaults["STATISTICS_BAR"])
calendar.add_component(
    Component(
        content=[
            date_picker := ft.DatePicker(
                on_change=change_date,
                on_dismiss=date_picker_dismissed,
                first_date=datetime.datetime(2023, 10, 1),
                last_date=datetime.datetime(2024, 10, 1),
            ),
            date_button := ft.ElevatedButton(
                "Pick date",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: date_picker.pick_date(),
            ),
        ],
        description="View representing calendar.",
    )
)
calendar.add_component(defaults["NAVIGATION_BAR"])
print(calendar)
