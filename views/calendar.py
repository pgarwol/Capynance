import utils.services as services
from session import Session
from views.view import View
from utils.styles import Style
from components.component import Component
from components.default_components import defaults
import datetime
import flet as ft


def change_date():
    calendar.var["savings_deadline"] = date_picker.value
    calendar.var["savings_deadline_output"].value = f"{date_picker.value:%d-%m-%Y}"
    if "page" in calendar.var:
        calendar.var["page"].update()


calendar = View(name="calendar", route="/calendar")


def init() -> None: ...


statistics = defaults["STATISTICS_BAR"]
main_content = Component(
    content=[
        date_picker := ft.DatePicker(
            on_change=lambda _: change_date(),
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        ),
        goal_textfield := ft.TextField(
            label=None,
            **Style.TextField.value,
        ),
        ft.Row(
            controls=[
                amount_textfield := ft.TextField(
                    label=None,
                    **Style.TextField.value,
                ),
                currency_dropdown := ft.Dropdown(
                    options=[
                        ft.dropdown.Option("ZŁ"),
                        ft.dropdown.Option("EUR"),
                        ft.dropdown.Option("USD"),
                        ft.dropdown.Option("GBP"),
                    ],
                    label=None,
                    **Style.Dropdown.value,
                ),
            ]
        ),
        ft.Row(
            controls=[
                date_textfield := ft.TextField(
                    label=None,
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
        add_button := ft.ElevatedButton(
            text=None,
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
data_row = Component(
    content=[
        ft.DataTable(
            sort_ascending=True,
            columns=[
                ft.DataColumn(date_col_header := ft.Text(value=None)),
                ft.DataColumn(goal_col_header := ft.Text(value=None)),
                ft.DataColumn(amount_col_header := ft.Text(value=None), numeric=True),
            ],
            rows=[],
        )
    ],
    description="User finance goals",
)
navbar = defaults["NAVIGATION_BAR"]

calendar.add_component(statistics)
calendar.add_component(main_content)
calendar.add_component(data_row)
calendar.add_component(navbar)

calendar.var = {
    "savings_goal": calendar.components[1].content[1],
    "savings_amount": calendar.components[1].content[2].controls[0],
    "savings_currency": calendar.components[1].content[2].controls[1],
    "savings_deadline_output": calendar.components[1].content[3].controls[0],
}


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
    Session.get_logged_user().from_savings_datarow(
        date=f"{date:%d-%m-%Y}",
        goal=goal,
        amount=f"{amount:.2f}",
        currency=currency,
    )
    if not Session.get_logged_user().does_savings_goal_exist(goal):
        services.save_user_data(Session.get_logged_user())

    if "page" in calendar.var:
        calendar.var["page"].update()


# TODO
def remove_savings_row(row) -> None: ...


def retrieve_dto_data(dto) -> None:
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
    retrieve_dto_data(dto=Session.get_logged_user())


def refresh_labels() -> None:
    goal_textfield.label = calendar.lang["goal"]
    currency_dropdown.label = calendar.lang["currency"]
    amount_textfield.label = calendar.lang["amount"]
    date_textfield.label = calendar.lang["date"]
    add_button.text = calendar.lang["add"]
    date_col_header.value = calendar.lang["date"]
    amount_col_header.value = calendar.lang["amount"]
    goal_col_header.value = calendar.lang["goal"]


refresh_labels()

calendar.refresh_language_contents = refresh_labels

print(calendar)
