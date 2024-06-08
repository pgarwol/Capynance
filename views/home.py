import datetime
import logging
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
from utils.sync_manager import SyncManager
from utils.theme_manager import ThemeManager
from views import reset_calendar, reset_finances
from views.view import View, ViewsInitialStates

# Global variables
spending_dict = {}
header_size = 26
header_weight = ft.FontWeight.W_400
daily_tip = None


def refresh_labels() -> None:
    """
    This function changes view's texts based on the current language.

    :return: None
    """
    daily_tip_header.value = home.lang["daily_tip_header"]
    daily_tip_text.value = generate_daily_tip()
    text_achievements.value = home.lang["achievements"]
    last_speding_header.value = home.lang["last_spending"]
    next_aim_text.value = home.lang["next_goal"]
    btn_settings.text = home.lang["app_settings"]
    btn_log_out.text = home.lang["log_out"]
    txt_add_spending.value = (home.lang["add_spending"])
    txt_spending_desc.value = home.lang["spending_desc"]
    txt_spending_value.value = home.lang["spending_value"]
    manual_spending_dialog.actions[0].text = home.lang["cancel"]
    manual_spending_dialog.actions[1].text = home.lang["confirm"]


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
    services.save_all_data(Session.get_logged_user())
    DefaultComponents.NAVIGATION_BAR.value.content[0].selected_index = (
        DefaultComponents.DEFAULT_MENU_SELECTION.value
    )
    Page.go("/")
    reset_calendar()
    reset_finances()
    Page.update()


# Elements depending on the theme mode. Their colors are controlled by the LocalThemeManager class.
theme_dependent_elements = [
    icon_attach_money := ft.Icon(name=ft.icons.ATTACH_MONEY, color=ft.colors.BLACK),
    icon_savings_outlined := ft.Icon(
        name=ft.icons.SAVINGS_OUTLINED, color=ft.colors.BLACK, size=60
    ),
    icon_flag_circle_outlined := ft.Icon(
        name=ft.icons.FLAG_CIRCLE_OUTLINED, color=ft.colors.BLACK, size=60
    ),
    btn_settings := ft.ElevatedButton(
        text="Ustawienia aplikacji",
        on_click=go_to_settings,
        width=200,
        bgcolor=ft.colors.GREY_200,
        color=ft.colors.BLACK,
    ),
    btn_log_out := ft.ElevatedButton(
        text="Wyloguj się",
        on_click=log_user_out,
        width=200,
        bgcolor=ft.colors.GREY_200,
        color=ft.colors.BLACK,
    ),
]


class TipsOfTheDay(Enum):
    """Enumeration for daily tips."""

    TIP_1 = {
        "pl": "Codziennie odkładając choćby niewielką kwotę, budujesz swoją finansową przyszłość",
        "en": "By saving even a small amount every day, you build your financial future"
    }
    TIP_2 = {
        "pl": "Planuj wydatki z wyprzedzeniem, aby uniknąć niepotrzebnych zakupów",
        "en": "Plan your expenses in advance to avoid unnecessary purchases"
    }
    TIP_3 = {
        "pl": "Korzystaj z promocji, ale tylko wtedy, gdy faktycznie potrzebujesz produktu",
        "en": "Take advantage of promotions, but only if you really need the product"
    }
    TIP_4 = {
        "pl": "Unikaj impulsywnych zakupów – zrób listę przed wyjściem do sklepu",
        "en": "Avoid impulsive purchases – make a list before going to the store"
    }
    TIP_5 = {
        "pl": "Ustal miesięczny budżet i trzymaj się go",
        "en": "Set a monthly budget and stick to it"
    }
    TIP_6 = {
        "pl": "Przygotowuj posiłki w domu zamiast jeść na mieście",
        "en": "Prepare meals at home instead of eating out"
    }
    TIP_7 = {
        "pl": "Oszczędzaj energię – wyłączaj światła i urządzenia, gdy ich nie używasz",
        "en": "Save energy – turn off lights and devices when not in use"
    }
    TIP_8 = {
        "pl": "Regularnie przeglądaj swoje subskrypcje i rezygnuj z nieużywanych",
        "en": "Regularly review your subscriptions and cancel unused ones"
    }
    TIP_9 = {
        "pl": "Zainwestuj w jakość – lepsze produkty często służą dłużej",
        "en": "Invest in quality – better products often last longer"
    }
    TIP_10 = {
        "pl": "Oszczędzaj na dużych zakupach, polując na sezonowe wyprzedaże",
        "en": "Save on big purchases by hunting for seasonal sales"
    }


class LocalThemeManager:
    """
    The LocalThemeManager class is responsible for managing the theme of the application at a home view level.
    It updates the color of the icons based on the current theme mode.
    """

    def __init__(self, theme: ft.ThemeMode):
        """
        Initializes a new instance of the LocalThemeManager class.

        Args:
            theme (ft.ThemeMode): The initial theme mode of the application.
        """
        self.theme_mode = theme

    def on_change_theme(self, theme: ft.ThemeMode):
        """
        Changes the theme of the application and updates the color of the icons.

        Args:
            theme (ft.ThemeMode): The new theme mode of the application.
        """
        self.theme_mode = theme

        # Update the icon color based on the theme mode
        for element in theme_dependent_elements:
            element.color = (
                ft.colors.BLACK if theme == ft.ThemeMode.LIGHT else ft.colors.WHITE
            )

        # Additional theme-dependent settings
        btn_settings.bgcolor = (
            ft.colors.GREY_200 if theme == ft.ThemeMode.LIGHT else ft.colors.GREY_800
        )
        btn_log_out.bgcolor = (
            ft.colors.GREY_200 if theme == ft.ThemeMode.LIGHT else ft.colors.GREY_800
        )


def generate_daily_tip() -> str:
    """
    This function generates a daily tip for the user.

    It randomly selects a tip from the TipsOfTheDay enumeration and creates a text with the selected tip and
    the current language of the logged-in user.

    Returns:
        str: A text component with the daily tip.
    """

    global daily_tip

    # Randomly select a tip from the TipsOfTheDay enumeration
    if daily_tip is None:
        daily_tip = random.choice(list(TipsOfTheDay)).value

    return daily_tip[Session.language]


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
    try:
        e.page.dialog = manual_spending_dialog
        manual_spending_dialog.open = True
        e.page.update()
    except Exception as e:
        print(f"An error occurred: {e}")


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
    tf_spending_desc.value = ""
    tf_spending_value.value = ""


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

    # Parse float from spending value
    value = tf_spending_value.value
    if "," in value:
        value = value.replace(",", ".")
    if value.count(".") > 1:
        value = value.replace(".", "", value.count(".") - 1)
    if value.isspace():
        logging.error("Spending value is empty. Skipping adding spending.")
        clear_manual_spending_dialog()
        return
    if value.isalpha():
        logging.error("Spending value is not a number. Skipping adding spending.")
        clear_manual_spending_dialog()
        return
    if not value:
        logging.error("Spending value is empty. Skipping adding spending.")
        clear_manual_spending_dialog()
        return
    try:
        value = float(value)
    except ValueError:
        logging.error("Spending value is not a number. Skipping adding spending.")
        clear_manual_spending_dialog()
        return

    description = tf_spending_desc.value
    if description.isspace():
        logging.error("Spending description is empty. Skipping adding spending.")
        clear_manual_spending_dialog()
        return
    if not description:
        logging.error("Spending description is empty. Skipping adding spending.")
        clear_manual_spending_dialog()
        return

    spending_dict["spending"][
        datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    ] = [description, value]

    # Update spending dict in user DTO
    Session.get_logged_user().manual_spending = spending_dict
    SyncManager.sync_manual_spending()  # Sync data with database

    clear_manual_spending_dialog()


manual_spending_dialog = ft.AlertDialog(
    True,
    txt_add_spending := ft.Text("Wprowadź wydatek"),
    content=ft.Container(
        content=ft.Column(
            controls=[
                txt_spending_desc := ft.Text("Opis wydatku"),
                tf_spending_desc := ft.TextField(),
                txt_spending_value := ft.Text("Kwota"),
                tf_spending_value := ft.TextField(keyboard_type=KeyboardType.NUMBER),
            ]
        ),
        height=300,
    ),
    actions=[
        ft.TextButton(
            text="Anuluj",
            on_click=discard_manual_spending_dialog,
            style=ft.ButtonStyle(color=ft.colors.RED),
        ),
        ft.TextButton(
            text="Zatwierdź",
            on_click=confirm_manual_spending_dialog,
            style=ft.ButtonStyle(color=Colors.PRIMARY_DARKER),
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)


def retrieve_dto_profile(dto: user.User) -> None:
    """
    This function retrieves the profile data for a given user and updates the user data section with name, surname and
    email.

    :param dto: User data transfer object.
    :return: None
    """
    view_data = services.get_view_data(view_name="profile", user_id=dto.id)
    if "first_name" not in view_data or "last_name" not in view_data:
        logging.error(
            "First name or last name not found in view data. User data will not be filled at home page."
        )
        return
    cont_usr_data.content.controls[0].value = (
            view_data["first_name"] + " " + view_data["last_name"]
    )
    cont_usr_data.content.controls[1].value = view_data["email"]


def retrieve_dto_data(dto: user.User) -> None:
    """
    This function retrieves the data for a given user.
    It calls three other functions to retrieve the profile, spending, and calendar data for the user.

    :param dto: User data transfer object.
    :return: None
    """
    retrieve_dto_profile(dto)
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
    view_data = services.get_view_data(view_name="manual-spending", user_id=dto.id)
    if "spending" not in view_data:
        logging.warning(
            "Spending data not found in view data. Spending data will not be filled at home page."
        )
        view_data["spending"] = {}
        logging.warning("Initializing empty spending data in user DTO.")
        spending_dict = view_data
        return
    spending_dict = view_data
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
    view_data = services.get_view_data(view_name="calendar", user_id=dto.id)
    if "savings_rows" not in view_data:
        return
    aims_dict = view_data["savings_rows"]

    # Iterate over the entries to find the closest deadline
    today = datetime.datetime.now()
    closest_entry = None
    min_diff = float("inf")
    for key, value in aims_dict.items():
        deadline = datetime.datetime.strptime(value["savings_deadline"], "%d-%m-%Y")
        diff = (deadline - today).days
        if 0 < diff < min_diff:
            min_diff = diff
            closest_entry = value

    cont_aim_controls.clear()
    # noinspection SpellCheckingInspection
    cont_aim_controls.append(icon_flag_circle_outlined)
    cont_aim_controls.append(
        ft.Text(
            "{:.2f} {}".format(
                float(closest_entry["savings_amount"]),
                closest_entry["savings_currency"],
            ),
            size=18,
            weight=ft.FontWeight.W_300,
        )
    )
    cont_aim_controls.append(
        ft.Text(
            value=closest_entry["savings_goal"],
            size=18,
            weight=ft.FontWeight.W_300,
            text_align=ft.TextAlign.CENTER,
        )
    )


def init_home() -> None:
    """
    This function initializes the home page of the application.

    It clears the spending rows and the aim controls, retrieves the data of the logged-in user, and sets up the theme.

    The theme setup involves creating a LocalThemeManager instance with the current theme mode and adding it as an
    observer to the ThemeManager.

    Returns:
        None
    """
    # Clear the spending rows and the aim controls
    spending_rows.clear()
    cont_aim_controls.clear()

    # Retrieve the data of the logged-in user
    retrieve_dto_data(dto=Session.get_logged_user())

    # Set up the theme
    # Create a LocalThemeManager instance with the current theme mode
    theme_info = LocalThemeManager(ThemeManager.theme_mode)
    # Add the LocalThemeManager instance as an observer to the ThemeManager
    ThemeManager.add_observer(theme_info)
    theme_info.on_change_theme(theme_info.theme_mode)

    refresh_labels()


def read_latest_spending(spending: dict[str, dict[list[str, float]]]) -> None:
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
    spending = spending["spending"]
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

    It takes the spending data and the row index as input and creates a row with an icon, a text container for the
    name of the spending item, and a text for the price of the spending item.

    Args:
        spending_item (tuple[str, float]): A tuple containing the name and price of the spending item.

    Returns:
        ft.Row: A row component for the spending item.
    """
    return ft.Row(
        [
            # An icon element for the spending item.
            icon_attach_money,
            # A text container for the name of the spending item.
            ft.Container(
                ft.Text(spending_item[0], size=18, weight=ft.FontWeight.W_300),
                width=200,
            ),
            # A text for the price of the first spending item.
            ft.Text(
                "{:.2f} zł".format(spending_item[1]),
                size=18,
                weight=ft.FontWeight.W_300,
            ),
        ],
        spacing=10,
    )


# A container for user data. It displays the user's full name and username.
cont_usr_data = ft.Container(
    # A column is used to arrange the text vertically.
    ft.Column(
        [
            # The user's full name
            ft.Text("Imię i nazwisko", size=35, weight=ft.FontWeight.W_300),
            # The user's username
            ft.Text("Nick1234", size=18, weight=ft.FontWeight.W_400),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    ),
    alignment=ft.alignment.center,
)

# A container for the daily tip section on the home page.
# noinspection SpellCheckingInspection
cont_daily_tip = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the daily tip section.
            daily_tip_header := ft.Text("Porada dnia", size=header_size, weight=header_weight),

            ft.Container(
                daily_tip_text := ft.Text(
                    value='Daily tip',
                    size=18,
                    no_wrap=False,
                    italic=True,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(5),
            ),
            # A container for an image element.
            ft.Container(icon_savings_outlined, alignment=ft.alignment.center),
        ],
        alignment=ft.MainAxisAlignment.START,
    )
)

# A container for the achievements section on the home page.
# noinspection SpellCheckingInspection
cont_achievements = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the achievements section.
            text_achievements := ft.Text("Osiągnięcia", size=header_size, weight=header_weight),
            # A container for an image element.
            ft.Container(
                ft.Row(
                    [
                        ft.Image(
                            src="https://lh3.googleusercontent.com/pw/AP1GczOOgFmCBvJQh"
                                "-e6wNXInYOQoIuunFvNeHWNA4Jsu8mHYKuH3NRbP-ltRJVDn5SvcXdoKP6aQKv-d_zyWE7I"
                                "-xMKqo0XXeMleaPzO_lewGRxHIYtZgk0A4dWiVW18LYF9F7xNxwXTjzR886GnI74R1E=w968-h968-s-no"
                                "?authuser=0",
                            width=60,
                            height=60,
                        ),
                        ft.Image(
                            src="https://lh3.googleusercontent.com/pw/AP1GczNHLgqYtKf6R6758jqUfcQh6AtfS6oqpEkXFMj2tEg"
                                "zw9KssDInmp7CG_htmF3yghFzpg7yehkSpyqe2jYKc3aHPCXugJMIrGz7EzPZch_c0uIaM2-QAe3uj56A5IhC"
                                "81ZaZ4N5cJJzCOsJZYsB7Wg=w894-h894-s-no-gm?authuser=0",
                            width=60,
                            height=60,
                        ),
                    ]
                ),
                padding=ft.padding.all(13),
                border=ft.border.all(width=2, color="#33A9A9A9"),
                border_radius=ft.border_radius.all(20),
                bgcolor="#33bab8b8",
                alignment=ft.alignment.center,
                margin=10,
                width=500,
            ),
        ],
    ),
)

# Spending section
# noinspection SpellCheckingInspection
cont_spending = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the spending section.
            last_speding_header := ft.Text("Ostatnie wydatki", size=header_size, weight=header_weight),
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
            next_aim_text := ft.Text("Nadchodzący cel", size=header_size, weight=header_weight),
            # A container for the goal details. It consists of a column of elements: an image, a text for the goal
            # amount, and a text for the goal description.
            ft.Container(
                ft.Column(
                    cont_aim_controls := [],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                alignment=ft.alignment.center,
            ),
        ],
    )
)

# A container for the last buttons section on the home page.
cont_last_buttons = ft.Container(
    ft.Column(
        [
            # An elevated button for the application settings.
            btn_settings,
            # An elevated button for the logout action.
            btn_log_out,
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
                expand=True,
            ),
            btn_add_spending_manual,
        ],
        "Home page",
    )
)


home.add_component(DefaultComponents.NAVIGATION_BAR.value)
home.refresh_language_contents = refresh_labels
ViewsInitialStates.set_home_copy(home)
home.log()
