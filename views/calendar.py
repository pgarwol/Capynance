from components.default_components import defaults
from components.component import Component
from views.view import View
from utils.global_enums import String
from typing import Tuple
import datetime
from utils.colors import Color
from utils.styles import Style
from views.login import login
import flet as ft


calendar = View(name="calendar", route="/calendar")
calendar.add_component(defaults["STATISTICS_BAR"])
calendar.add_component(
    Component(
        content=[
            date_picker := ft.DatePicker(
                on_change=lambda _: change_date(),
                first_date=datetime.datetime(2023, 10, 1),
                last_date=datetime.datetime(2024, 10, 1),
            ),
            ft.TextField(
                label="Cel",
                **Style.TextField.value,
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        label="Ilość",
                        **Style.TextField.value,
                    ),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("ZŁ"),
                            ft.dropdown.Option("EUR"),
                            ft.dropdown.Option("USD"),
                            ft.dropdown.Option("GBP"),
                        ],
                        label="Waluta",
                        **Style.Dropdown.value,
                    ),
                ]
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        label="Data",
                        read_only=True,
                        **Style.TextField.value,
                    ),
                    date_button := ft.IconButton(
                        icon=ft.icons.CALENDAR_MONTH,
                        on_click=lambda _: date_picker.pick_date(),
                        **Style.IconButton.value,
                    ),
                ]
            ),
            ft.ElevatedButton(
                text="Dodaj",
                on_click=lambda _: add_savings_row(
                    date=calendar.var["savings_deadline"],
                    goal=calendar.var["savings_goal"].value,
                    amount=calendar.var["savings_amount"].value,
                    currency=calendar.var["savings_currency"].value,
                ),
                **Style.ElevatedButton.value,
            ),
        ],
        description="User calendar inputs",
    )
)
calendar.var = {
    "savings_goal": calendar.components[1].content[1],
    "savings_amount": calendar.components[1].content[2].controls[0],
    "savings_currency": calendar.components[1].content[2].controls[1],
    "savings_deadline_output": calendar.components[1].content[3].controls[0],
}
calendar.add_component(
    Component(
        content=[
            ft.DataTable(
                sort_ascending=True,
                columns=[
                    ft.DataColumn(ft.Text("Data")),
                    ft.DataColumn(ft.Text("Cel")),
                    ft.DataColumn(ft.Text("Ilość"), numeric=True),
                    # ft.DataColumn(ft.Text(String.EMPTY.value)),
                ],
                rows=[],
            )
        ],
        description="User finance goals",
    )
)
calendar.add_component(defaults["NAVIGATION_BAR"])


def add_savings_row(date: datetime, goal: str, amount: str, currency: str) -> None:
    if goal is None or amount is None:
        return
    if date is None:
        date = datetime.datetime.now()
    if currency is None:
        currency = "ZŁ"

    try:
        amount = round(float(amount), 2)
    except ValueError:
        return

    calendar.get_component(2).content[0].rows.append(
        ft.DataRow(
            on_long_press=lambda row: remove_savings_row(row),
            cells=[
                ft.DataCell(ft.Text(f"{date:%d-%m-%Y}")),
                ft.DataCell(ft.Text(goal)),
                ft.DataCell(ft.Text(f"{amount:.2f} {currency}")),
            ],
        )
    )

    if "page" in calendar.var:
        calendar.var["page"].update()


def change_date():
    calendar.var["savings_deadline"] = date_picker.value
    calendar.var["savings_deadline_output"].value = f"{date_picker.value:%d-%m-%Y}"
    if "page" in calendar.var:
        calendar.var["page"].update()


# TODO
def remove_savings_row(row) -> None: ...


print(calendar)
