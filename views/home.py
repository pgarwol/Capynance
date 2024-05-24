import datetime
import random
from enum import Enum

import flet as ft
import flet_core.control_event
from flet_core import KeyboardType

import user
from components.component import Component, DefaultComponents
from page import Page
from session import Session
from utils import services
from utils.enums import FletNames, Colors
from views import reset_calendar, reset_finances
from views.view import View, ViewsInitialStates


class TipsOfTheDay(Enum):
    """Enumeration for daily tips."""
    TIP_1 = 'Codziennie odkładając choćby niewielką kwotę, budujesz swoją finansową przyszłość'
    TIP_2 = 'Planuj wydatki z wyprzedzeniem, aby uniknąć niepotrzebnych zakupów'
    TIP_3 = 'Korzystaj z promocji, ale tylko wtedy, gdy faktycznie potrzebujesz produktu'
    TIP_4 = 'Unikaj impulsywnych zakupów – zrób listę przed wyjściem do sklepu'
    TIP_5 = 'Ustal miesięczny budżet i trzymaj się go'
    TIP_6 = 'Przygotowuj posiłki w domu zamiast jeść na mieście'
    TIP_7 = 'Oszczędzaj energię – wyłączaj światła i urządzenia, gdy ich nie używasz'
    TIP_8 = 'Regularnie przeglądaj swoje subskrypcje i rezygnuj z nieużywanych'
    TIP_9 = 'Zainwestuj w jakość – lepsze produkty często służą dłużej'
    TIP_10 = 'Oszczędzaj na dużych zakupach, polując na sezonowe wyprzedaże'


spending_dict = {}


def generate_daily_tip() -> ft.Container:
    """
    This function generates a daily tip for the user.

    It randomly selects a tip from the TipsOfTheDay enumeration and creates a text container with the selected tip.

    Returns:
        ft.Container: A container with the daily tip text.
    """

    # Randomly select a tip from the TipsOfTheDay enumeration
    text = random.choice(list(TipsOfTheDay)).value

    # Create a text container with the selected tip
    return ft.Container(
        ft.Text(text, size=15, no_wrap=False, italic=True, text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
        padding=ft.padding.all(5),
    )


def add_spending_manual(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function opens a dialog for manual spending input.

    It sets the current page's dialog to the manual spending dialog and opens it.
    After that, it updates the page to reflect these changes.

    Args:
        e (flet_core.control_event.ControlEvent): The event object that triggered this function.

    Returns:
        None
    """
    e.page.dialog = manual_spending_dialog
    manual_spending_dialog.open = True
    e.page.update()


def discard_manual_spending_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function closes the manual spending input dialog.

    It sets the 'open' attribute of the current page's dialog to False, effectively closing it.
    After that, it updates the page to reflect these changes and clears the dialog.

    Args:
        e (flet_core.control_event.ControlEvent): The event object that triggered this function.

    Returns:
        None
    """
    e.page.dialog.open = False
    e.page.update()
    clear_manual_spending_dialog()


def clear_manual_spending_dialog() -> None:
    """
    This function clears the manual spending input dialog.

    It sets the 'value' attribute of the 'tf_spending_desc' and 'tf_spending_value' text fields to an empty string,
    effectively clearing the input fields in the dialog.

    Returns:
        None
    """
    tf_spending_desc.value = ''
    tf_spending_value.value = ''


def confirm_manual_spending_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function confirms the manual spending input dialog.

    It sets the 'open' attribute of the current page's dialog to False, effectively closing it.
    After that, it updates the page to reflect these changes.
    It then adds the spending description and value to the global spending dictionary with the current date as the key.
    Finally, it updates the spending display and clears the dialog.

    Args:
        e (flet_core.control_event.ControlEvent): The event object that triggered this function.

    Returns:
        None
    """
    global spending_dict
    e.page.dialog.open = False
    e.page.update()
    spending_dict[datetime.datetime.now().strftime('%Y-%m-%d')] = \
        [tf_spending_desc.value, float(tf_spending_value.value)]
    read_latest_spending(spending_dict)
    clear_manual_spending_dialog()


manual_spending_dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Wprowadź wydatek"),
    content=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Opis wydatku'),
                tf_spending_desc := ft.TextField(),
                ft.Text('Kwota'),
                tf_spending_value := ft.TextField(keyboard_type=KeyboardType.NUMBER),
            ]
        ),
        height=300,
    ),
    actions=[
        ft.TextButton(
            text="Anuluj",
            on_click=discard_manual_spending_dialog,
            style=ft.ButtonStyle(color=ft.colors.RED)
        ),
        ft.TextButton(
            text="Zatwierdź",
            on_click=confirm_manual_spending_dialog,
            style=ft.ButtonStyle(color=Colors.PRIMARY_DARKER)
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)


def retrieve_dto_data(dto: user.User) -> None:
    retrieve_dto_spending(dto)
    retrieve_dto_calendar(dto)


def retrieve_dto_spending(dto) -> None:
    """
    This function retrieves the spending data for a given user.

    It calls the get_view_data function from the services module, passing in 'manual-spending' as the view name and the
    id of the user as the user_id. The function returns a dictionary containing the view data for the user.

    If 'spending' is not in the view data, the function returns None. Otherwise, it updates the global spending_dict
    with the spending data from the view data and calls the read_latest_spending function, passing in the updated
    spending_dict.

    Args:
        dto: The data transfer object (DTO) of the user.

    Returns:
        None
    """
    global spending_dict
    view_data = services.get_view_data(view_name='manual-spending', user_id=dto.id)
    if 'spending' not in view_data:
        return
    spending_dict = view_data['spending']
    read_latest_spending(spending_dict)


def retrieve_dto_calendar(dto: user.User) -> None:
    """
    This function retrieves the calendar data for a given user and updates the upcoming goal section.

    It calls the get_view_data function from the services module, passing in 'calendar' as the view name and the
    id of the user as the user_id. The function returns a dictionary containing the view data for the user.

    If 'savings_rows' is not in the view data, the function returns None. Otherwise, it iterates over the entries
    to find the closest deadline and updates the upcoming goal section with the closest entry.

    Args:
        dto: The data transfer object (DTO) of the user.

    Returns:
        None
    """
    view_data = services.get_view_data(view_name='calendar', user_id=dto.id)
    if 'savings_rows' not in view_data:
        return
    aims_dict = view_data['savings_rows']

    # Iterate over the entries to find the closest deadline
    today = datetime.datetime.today()
    closest_entry = None
    min_diff = float('inf')
    for key, value in aims_dict.items():
        deadline = datetime.datetime.strptime(value["savings_deadline"], "%d-%m-%Y")
        diff = (deadline - today).days
        if 0 < diff < min_diff:
            min_diff = diff
            closest_entry = value

    cont_aim_controls.clear()
    # noinspection SpellCheckingInspection
    cont_aim_controls.append(
        ft.Image(
            src='https://lh3.googleusercontent.com/pw'
                '/AP1GczM7EACZEZZFYqXj4fxQg4Ywi8cMId_Y7WQqGgFyoglA1knlUff4ARnsnItRMClxxI5Xea'
                'DRJsqqYWowsS1zi_vhxpkgqXDfGy7ZIXMtpLRxxow_MR1ycO-gGkc8TTjb6IdfYKVyU19VJLhzmpJQjSQ'
                '=w96-h96-s-no?authuser=0', width=50, height=50
        )
    )
    cont_aim_controls.append(
        ft.Text('{:.2f} {}'.format(
            float(closest_entry['savings_amount']),
            closest_entry['savings_currency']
        ),
            size=18,
            weight=ft.FontWeight.W_300
        )
    )
    cont_aim_controls.append(
        ft.Text(
            value=closest_entry['savings_goal'],
            size=18,
            weight=ft.FontWeight.W_300,
            text_align=ft.TextAlign.CENTER,
        )
    )


def init_home() -> None:
    """
    This function initializes the home page.

    It clears the spending rows and the upcoming goal section.
    After that, it retrieves the data for the logged-in user.

    Returns:
        None
    """
    spending_rows.clear()
    cont_aim_controls.clear()
    retrieve_dto_data(dto=Session.get_logged_user())


def read_latest_spending(spending: dict[str, list[str, float]]) -> None:
    """
    This function reads the latest spending data and updates the spending rows.

    It sorts the dates in the spending dictionary in descending order and selects the three latest dates.
    It then retrieves the spending items for these dates and generates spending rows for them.
    Finally, it updates the page to reflect these changes.

    Args:
        spending (dict[str, list[str, float]]): A dictionary where the keys are dates in the format 'YYYY-MM-DD' and
        the values are lists containing the spending description and value.

    Returns:
        None
    """
    sorted_dates = sorted(spending.keys(), reverse=True)
    latest_three = sorted_dates[:3]
    latest_spending = [(spending[date][0], spending[date][1]) for date in latest_three]
    # Generate spending rows for the latest spending items
    spending_rows.clear()
    for spending_item in latest_spending:
        spending_rows.append(generate_one_spending_row(spending_item))
    Page.update()


# noinspection SpellCheckingInspection
def generate_one_spending_row(spending_item: tuple[str, float]) -> ft.Row:
    """
    This function generates a row for a single spending item.

    It takes the spending data and the row index as input and creates a row with an image, a text container for the
    name of the spending item, and a text for the price of the spending item.

    Args:
        spending_item (tuple[str, float]): A tuple containing the name and price of the spending item.

    Returns:
        ft.Row: A row component for the spending item.
    """
    return ft.Row(
        [
            # An image element for the spending item.
            ft.Image(
                src='https://lh3.googleusercontent.com/pw/AP1GczPpl6AesgZTckABVSRVT92dOr6IxMqJc1BsJbKCzslMsT'
                    '-nMzA3A6Pg4Rhy-DtHnbm5m1XXTAvOLY77sEon5vP5c6sPsM6fKubxz8zKwpr'
                    '-du54fqApnv254ENnVldmCHumzpa2DD1xsxfSFJi3-iY=w96-h96-s-no?authuser=0',
                width=25,
                height=25,
            ),
            # A text container for the name of the spending item.
            ft.Container(
                ft.Text(spending_item[0], size=18, weight=ft.FontWeight.W_300),
                width=200,
            ),
            # A text for the price of the first spending item.
            ft.Text('{:.2f} zł'.format(spending_item[1]), size=18, weight=ft.FontWeight.W_300),
        ],
        spacing=10,
    )


# Placeholder functions for the button actions
def go_to_settings(_: flet_core.control_event.ControlEvent) -> None:
    """
    This function navigates to the settings page.

    It uses the Page.go method to navigate to the settings page. The route to the settings page is defined by the
    FletNames.SETTINGS constant.

    Args:
        _ : This argument is not used in the function.

    Returns:
        None
    """
    Page.go(f"/{FletNames.SETTINGS}")


def log_user_out(_: flet_core.control_event.ControlEvent) -> None:
    """
    This function logs the user out of the application.

    It resets the selected index of the navigation bar to the default menu selection.
    It then resets the views, the calendar, and the finances.
    Finally, it updates the page to reflect these changes.

    Args:
        _ : This argument is not used in the function.

    Returns:
        None
    """
    DefaultComponents.NAVIGATION_BAR.value.content[0].selected_index = (
        DefaultComponents.DEFAULT_MENU_SELECTION.value
    )
    View.reset_views()
    reset_calendar()
    reset_finances()
    Page.update()


# A container for user data. It displays the user's full name and username.
cont_usr_data = ft.Container(
    # A column is used to arrange the text vertically.
    ft.Column(
        [
            # The user's full name
            ft.Text('Imię i nazwisko', size=35, weight=ft.FontWeight.W_300),
            # The user's username
            ft.Text('Nick1234', size=18, weight=ft.FontWeight.W_400),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    ),
    alignment=ft.alignment.center,
)

# A container for the daily tip section on the home page.
# noinspection SpellCheckingInspection
cont_daily_tip = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the daily tip section.
            ft.Text('Porada dnia', size=25, weight=ft.FontWeight.W_200),

            # A function call to generate_daily_tip() which returns a container with the daily tip text.
            generate_daily_tip(),

            # A container for an image element.
            ft.Container(
                ft.Image(
                    src='https://lh3.googleusercontent.com/pw/AP1GczM0K4wwX7bUbCQFyJY5Q4rqNmI93'
                        '-nlfYfVpKXI2XpDug5dq_v5nj7XPlK2yDW7KcMQRssnMTpEqcCra12kSV5I8farpkWmBLorTBcRtWdHPiPmm'
                        '-eIGbFXmDik5m9P0xQ1UwhackEFPguo2pWmUCI=w512-h512-s-no?authuser=0',
                    width=75,
                    height=75
                ),
                alignment=ft.alignment.center
            )
        ],
        alignment=ft.MainAxisAlignment.START
    )
)

# A container for the achievements section on the home page.
# noinspection SpellCheckingInspection
cont_achievements = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the achievements section.
            ft.Text('Osiągnięcia', size=25, weight=ft.FontWeight.W_200),

            # A container for an image element.
            ft.Container(
                ft.Row(
                    [
                        ft.Image(
                            src='https://lh3.googleusercontent.com/pw/AP1GczMFKtBRf4tjMcjFzfl'
                                '-IiaSNuy9cQm1mQTiMtMzvprCNBM14ANYb_BWgGGazk2yMvmJzM'
                                '-zwjaWks4U3iOjtZT5uWPa_9B_E1gw9svLCPIApesLesfIhyObC1MOzBB1tM13TXgcmHXD6j4-KS6Q_Hg'
                                '=w53-h50-s-no?authuser=0',
                            width=60,
                            height=60,
                        ),
                    ]
                ),
                padding=ft.padding.all(13),
                border=ft.border.all(2, ft.colors.GREY_300),
                border_radius=ft.border_radius.all(20),
                bgcolor=ft.colors.GREY_100,
                alignment=ft.alignment.center,
                margin=10
            )
        ]
    )
)

# Spending section
# noinspection SpellCheckingInspection
cont_spending = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the spending section.
            ft.Text('Ostatnie wydatki', size=25, weight=ft.FontWeight.W_200),

            # A container for the list of spending items. Each item is represented as a row of elements: an
            # image, a text container for the item name, and a text for the item price.
            ft.Container(
                ft.Column(spending_rows := []),
                padding=ft.padding.all(10),
            ),
        ]
    ),
)

# A container for the upcoming goal section on the home page.
# noinspection SpellCheckingInspection
cont_aim = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the upcoming goal section.
            ft.Text('Nadchodzący cel', size=25, weight=ft.FontWeight.W_200),

            # A container for the goal details. It consists of a column of elements: an image, a text for the goal
            # amount, and a text for the goal description.
            ft.Container(
                ft.Column(
                    cont_aim_controls := [],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                alignment=ft.alignment.center,
            )
        ],
    )
)

# A container for the last buttons section on the home page.
cont_last_buttons = ft.Container(
    ft.Column(
        [
            # An elevated button for the application settings.
            ft.ElevatedButton(
                text='Ustawienia aplikacji',
                on_click=go_to_settings,
                width=200,
                bgcolor=ft.colors.GREY_200,
                color=ft.colors.BLACK,
            ),
            # An elevated button for the logout action.
            ft.ElevatedButton(
                text='Wyloguj się',
                on_click=log_user_out,
                width=200,
                bgcolor=ft.colors.GREY_200,
                color=ft.colors.BLACK,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    alignment=ft.alignment.center,
)

# A floating action button for adding spending manually.
btn_add_spending_manual = ft.FloatingActionButton(
    icon=ft.icons.ADD,
    on_click=add_spending_manual,
    bgcolor=Colors.PRIMARY_DARKER,
    shape=ft.CircleBorder(),
)

home = View(name=FletNames.HOME, route=f"/{FletNames.HOME}")
home.add_component(DefaultComponents.STATISTICS_BAR.value)
home.add_component(
    Component(
        [
            ft.Column(
                [
                    cont_usr_data,
                    ft.Divider(),
                    cont_daily_tip,
                    ft.Divider(),
                    cont_achievements,
                    ft.Divider(),
                    cont_spending,
                    ft.Divider(),
                    cont_aim,
                    ft.Divider(),
                    cont_last_buttons,
                ],
                scroll=ft.ScrollMode.HIDDEN,
                expand=True
            ),
            btn_add_spending_manual,
        ], "Home page"
    )
)
home.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_home_copy(home)
home.log()
