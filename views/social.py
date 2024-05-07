from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


def add_friend_onclick(e) -> None:
    """Add a friend to the user's friend list. Currently testing purposes only."""
    print('Friend added!')


# Placeholder image
usr_img = ft.Image(
    src='https://www.rainforest-alliance.org/wp-content'
        '/uploads/2021/06/capybara-square-1.jpg.optimal.jpg',
    border_radius=ft.border_radius.all(100),
    height=150,
    width=150
)

# User basic info as name and surname, basic data etd. Also, a button to add friends.
usr_stats = ft.Column(
    [
        ft.Text('Imię i nazwisko', size=25),
        ft.Column(
            [
                ft.Text('Basic dane'),
                ft.Text('Lorem ipsum'),
            ],
            spacing=1
        ),
        ft.ElevatedButton('Add friends', on_click=add_friend_onclick),
    ],
    spacing=15
)

# Merge of user image and user stats
usr_data = ft.Row(
    [
        usr_img,
        usr_stats,
    ],
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    vertical_alignment=ft.CrossAxisAlignment.START,
)

# News feed with friends updates. Shows last 3 updates.
friends_updates_title = ft.Row([ft.Text('Friends updates', size=25)],
                               alignment=ft.MainAxisAlignment.START)
friends_updates = ft.Column(
    [
        friends_updates_title,
    ]
)

social = View(name="social", route="/social")
social.add_component(defaults["STATISTICS_BAR"])
social.add_component(Component([usr_data, ft.Divider(), friends_updates], "User data and image"))
social.add_component(defaults["NAVIGATION_BAR"])
