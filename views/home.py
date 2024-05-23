from components.component import Component, DefaultComponents
from utils.enums import FletNames, Colors
from views.view import View, ViewsInitialStates
from enum import Enum
import flet as ft
import random


class TipsOfTheDay(Enum):
    """
    This class is an enumeration that represents the tips of the day.

    It is a subclass of the Enum class provided by the enum module in Python.
    Each attribute of this class represents a tip of the day. The attribute's name is a unique identifier for the tip,
    and its value is the text of the tip.
    """
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


def add_spending_manual(_):
    print('Spending added manually')


def go_to_settings(_):
    print('Settings opened')


def log_out(_):
    print('Logged out')


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

# A container for the spending section on the home page.
# noinspection SpellCheckingInspection
cont_spending = ft.Container(
    ft.Column(
        [
            # A text element that serves as the title for the spending section.
            ft.Text('Ostatnie wydatki', size=25, weight=ft.FontWeight.W_200),

            # A container for the list of spending items. Each item is represented as a row of elements: an
            # image, a text container for the item name, and a text for the item price.
            ft.Container(
                ft.Column(
                    [
                        # A row for the first spending item.
                        ft.Row(
                            [
                                # An image element for the first spending item.
                                ft.Image(
                                    src='https://lh3.googleusercontent.com/pw'
                                        '/AP1GczPpl6AesgZTckABVSRVT92dOr6IxMqJc1BsJbKCzslMsT-nMzA3A6Pg4Rhy'
                                        '-DtHnbm5m1XXTAvOLY77sEon5vP5c6sPsM6fKubxz8zKwpr'
                                        '-du54fqApnv254ENnVldmCHumzpa2DD1xsxfSFJi3-iY=w96-h96-s-no?authuser=0',
                                    width=25,
                                    height=25,
                                ),
                                # A text container for the name of the first spending item.
                                ft.Container(
                                    ft.Text('Guma Turbo', size=18, weight=ft.FontWeight.W_300),
                                    width=200,
                                ),
                                # A text for the price of the first spending item.
                                ft.Text('0,50 zł', size=18, weight=ft.FontWeight.W_300),
                            ],
                        ),
                        # The following rows have the same structure.
                        ft.Row(
                            [
                                ft.Image(
                                    src='https://lh3.googleusercontent.com/pw'
                                        '/AP1GczPpl6AesgZTckABVSRVT92dOr6IxMqJc1BsJbKCzslMsT-nMzA3A6Pg4Rhy'
                                        '-DtHnbm5m1XXTAvOLY77sEon5vP5c6sPsM6fKubxz8zKwpr'
                                        '-du54fqApnv254ENnVldmCHumzpa2DD1xsxfSFJi3-iY=w96-h96-s-no?authuser=0',
                                    width=25,
                                    height=25,
                                ),
                                ft.Container(
                                    ft.Text('Draże korsarze XXL', size=18, weight=ft.FontWeight.W_300),
                                    width=200,
                                ),
                                ft.Text('4,47 zł', size=18, weight=ft.FontWeight.W_300),
                            ],
                        ),
                        ft.Row(
                            [
                                ft.Image(
                                    src='https://lh3.googleusercontent.com/pw'
                                        '/AP1GczPpl6AesgZTckABVSRVT92dOr6IxMqJc1BsJbKCzslMsT-nMzA3A6Pg4Rhy'
                                        '-DtHnbm5m1XXTAvOLY77sEon5vP5c6sPsM6fKubxz8zKwpr'
                                        '-du54fqApnv254ENnVldmCHumzpa2DD1xsxfSFJi3-iY=w96-h96-s-no?authuser=0',
                                    width=25,
                                    height=25,
                                ),
                                ft.Container(
                                    ft.Text('Guma Turbo', size=18, weight=ft.FontWeight.W_300),
                                    width=200,
                                ),
                                ft.Text('0,50 zł', size=18, weight=ft.FontWeight.W_300),
                            ],
                        )
                    ]
                ),
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
                    [
                        # This is an image element for the goal.
                        ft.Image(
                            src='https://lh3.googleusercontent.com/pw'
                                '/AP1GczM7EACZEZZFYqXj4fxQg4Ywi8cMId_Y7WQqGgFyoglA1knlUff4ARnsnItRMClxxI5Xea'
                                'DRJsqqYWowsS1zi_vhxpkgqXDfGy7ZIXMtpLRxxow_MR1ycO-gGkc8TTjb6IdfYKVyU19VJLhzmpJQjSQ'
                                '=w96-h96-s-no?authuser=0', width=50, height=50
                        ),
                        # This is a text for the goal amount.
                        ft.Text('4,28 zł', size=18, weight=ft.FontWeight.W_300),
                        # This is a text for the goal description.
                        ft.Text('Piwo po zdanej obronie', size=18, weight=ft.FontWeight.W_300),
                    ],
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
                on_click=log_out,
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
