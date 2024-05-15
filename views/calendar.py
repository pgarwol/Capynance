import services
from user import User
from session import Session
from views.view import View
from utils.styles import Style
from components.component import Component
from components.default_components import defaults
import datetime
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
                ],
                rows=[],
            )
        ],
        description="User finance goals",
    )
)
calendar.add_component(defaults["NAVIGATION_BAR"])


def add_savings_row(
    date: datetime.datetime, goal: str, amount: str, currency: str
) -> None:
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

    if amount < 0:
        # TODO: error feedback
        return

    if not calendar.var["session"].logged_user.does_savings_goal_exist(goal):
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
        calendar.var["session"].logged_user.from_savings_datarow(
            date=f"{date:%d-%m-%Y}",
            goal=goal,
            amount=f"{amount:.2f}",
            currency=currency,
        )
        services.save_user_data(calendar.var["session"].logged_user)

        if "page" in calendar.var:
            calendar.var["page"].update()
    else:
        ...
        # "TODO: user error output: SAVING GOAL ALREADY EXISTS


def change_date():
    calendar.var["savings_deadline"] = date_picker.value
    calendar.var["savings_deadline_output"].value = f"{date_picker.value:%d-%m-%Y}"
    if "page" in calendar.var:
        calendar.var["page"].update()


# TODO
def remove_savings_row(row) -> None: ...


def retrieve_dto_data(dto: User) -> None:
    view_data = services.get_view_data(view_name=calendar.name, user_id=dto.id)
    savings_rows = view_data["savings_rows"]
    insert_dto_data_to_datarows(savings_rows)


def insert_dto_data_to_datarows(data: dict):
    for key in data:
        add_savings_row(
            date=datetime.datetime.strptime(data[key]["savings_deadline"], "%d-%m-%Y"),
            goal=data[key]["savings_goal"],
            amount=float(data[key]["savings_amount"]),
            currency=data[key]["savings_currency"],
        )


def init_calendar() -> None:
    if "session" in calendar.var:
        retrieve_dto_data(dto=calendar.var["session"].logged_user)


print(calendar)
