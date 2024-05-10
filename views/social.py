from components.default_components import defaults
from components.component import Component
from views.view import View
from enum import Enum
import flet as ft
import random


# noinspection SpellCheckingInspection
class FixedFriendsUpdates(Enum):
    """All possible friends updates. These are predefined and won't be implemented as real updates."""
    FRIEND_1 = ('https://www.allthingswild.co.uk/wp-content/uploads/2019/11/capy.jpg', 'Co tam kapibary??')
    FRIEND_2 = ('https://www.columbuszoo.org/sites/default/files/styles/uncropped_xl/public/assets/tours/Capybara'
                '%200360%20-%20Amanda%20Carberry%2C%20Columbus%20Zoo%20and%20Aquarium%20%281%29.jpg?itok=6K8he2dl',
                'Siema, jestem kapibarą')
    FRIEND_3 = ('https://people.com/thmb/ovi1vkp7e_cTTPC5LglB_Ii83n0=/1500x0/filters:no_upscale():max_bytes('
                '150000):strip_icc():focal(149x0:151x2)/capybara-1-300-dbd2c51946de4b989723201dac1f20ff.jpg',
                'Jedzenieeee. Kocham jedzenie!')
    FRIEND_4 = ('https://upload.wikimedia.org/wikipedia/commons/thumb/3/34'
                '/Hydrochoeris_hydrochaeris_in_Brazil_in_Petr%C3%B3polis%2C_Rio_de_Janeiro%2C_Brazil_09.jpg/1200px'
                '-Hydrochoeris_hydrochaeris_in_Brazil_in_Petr%C3%B3polis%2C_Rio_de_Janeiro%2C_Brazil_09.jpg',
                'Kapibary są super!')
    FRIEND_5 = ('https://www.pwpark.com/wp-content/uploads/2023/12/sDSC_1067-copy-1024x1024.jpg', 'Dziś w zoo')
    FRIEND_6 = ('https://blog.nature.org/wp-content/uploads/2020/02/'
                '29555193323_15d785590f_k.jpg?w=1024', 'Jest pływane. Polecam bardzo')


def create_update(image_url: str, text: str) -> ft.Container:
    """
    Create a friend or own update with an image and text.

    This function creates a container with a row of two elements: an image and a text container.
    The image is created with the provided URL, a border radius of 100, and a fixed height and width of 50.
    The text container contains the provided text with a size of 15 and a left padding of 10.
    The row has a start alignment and a spacing of 10.
    The overall container has a left padding of 15.

    Parameters:
    image_url (str): The URL of the image to be displayed in the update.
    text (str): The text content of the update.

    Returns:
    ft.Container: A container representing the update.
    """
    if not image_url:
        raise ValueError('Image URL cannot be empty.')
    if not text:
        raise ValueError('Text cannot be empty.')

    if not isinstance(image_url, str):
        raise TypeError('Image URL must be a string.')
    if not isinstance(text, str):
        text = str(text)

    if not image_url.startswith('http'):
        raise ValueError('Image URL must start with "http" or "https".')

    if len(text) > 35:
        raise ValueError('Text cannot be longer than 35 characters.')

    return ft.Container(
        ft.Row(
            [
                ft.Image(
                    src=image_url,
                    border_radius=ft.border_radius.all(100),
                    height=50,
                    width=50
                ),
                ft.Container(
                    ft.Text(
                        text,
                        size=15,
                    ),
                    padding=ft.padding.only(left=10)
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        ), padding=ft.padding.only(left=15)
    )


def add_friend_onclick(_) -> None:
    """Add a friend to the user's friend list. Currently testing purposes only."""
    print('Friend added!')


def new_post_onclick(_) -> None:
    """Add a new post to the user's feed. Currently testing purposes only."""
    print('New post added!')


# Placeholder image
usr_img = ft.Image(
    src='https://www.rainforest-alliance.org/wp-content'
        '/uploads/2021/06/capybara-square-1.jpg.optimal.jpg',
    border_radius=ft.border_radius.all(100),
    height=150,
    width=150
)

# User basic info as name and surname, basic data etc. Also, a button to add friends.
usr_stats = ft.Column(
    [
        ft.Text('Imię i nazwisko', size=23, weight=ft.FontWeight.W_200),
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
friends_updates_title = ft.Container(ft.Row(
    [ft.Text('What\'s new?', size=25, weight=ft.FontWeight.W_200)],
    alignment=ft.MainAxisAlignment.START
))
list_of_updates = [create_update(update.value[0], update.value[1]) for update in random.sample(list(FixedFriendsUpdates), 3)]
list_of_updates.insert(0, friends_updates_title)
friends_updates = ft.Column(list_of_updates)

# Achievements section with images representing achievements
achievements_cont = ft.Container(
    ft.Row(
        [
            ft.Image(src='https://placehold.co/60x60/png'),
            ft.Image(src='https://placehold.co/60x60/png')
        ]
    ),
    padding=ft.padding.all(13),
    border=ft.border.all(2, ft.colors.GREY_300),
    border_radius=ft.border_radius.all(20),
    bgcolor=ft.colors.GREY_100,
    alignment=ft.alignment.center,
    margin=10
)
achievements = ft.Column(
    [
        ft.Text('Achievements', size=25, weight=ft.FontWeight.W_200),
        achievements_cont,
    ]
)

# Floating button to add a new post
new_post_btn = ft.FloatingActionButton(
    icon=ft.icons.ADD,
    on_click=new_post_onclick,
    bgcolor=ft.colors.RED_600,
    shape=ft.CircleBorder(),
)

social = View(name="social", route="/social")
social.add_component(defaults["STATISTICS_BAR"])
social.add_component(Component([
    ft.Column(
        [
            usr_data,
            ft.Divider(),
            friends_updates,
            ft.Divider(),
            achievements,
        ],
        scroll=ft.ScrollMode.HIDDEN,
        expand=True
    ),
    new_post_btn,
], "User data and image"))
social.add_component(defaults["NAVIGATION_BAR"])
