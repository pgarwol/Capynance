from utils.enums import FletNames
import utils.services as services
from components.component import Component, DefaultComponents
from views.view import View
import flet as ft


def add_friend_onclick(_) -> None:
    """Add a friend to the user's friend list. Currently testing purposes only."""
    print("Friend added!")


def new_post_onclick(_) -> None:
    """Add a new post to the user's feed. Currently testing purposes only."""
    print("New post added!")


# Placeholder image
usr_img = ft.Image(
    src="https://www.rainforest-alliance.org/wp-content"
    "/uploads/2021/06/capybara-square-1.jpg.optimal.jpg",
    border_radius=ft.border_radius.all(100),
    height=150,
    width=150,
)

# User basic info as name and surname, basic data etc. Also, a button to add friends.
usr_stats = ft.Column(
    [
        ft.Text("Imię i nazwisko", size=23, weight=ft.FontWeight.W_200),
        ft.Column(
            [
                ft.Text("Basic dane"),
                ft.Text("Lorem ipsum"),
            ],
            spacing=1,
        ),
        ft.ElevatedButton("Add friends", on_click=add_friend_onclick),
    ],
    spacing=15,
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
friends_updates_title = ft.Row(
    [ft.Text("What's new?", size=25, weight=ft.FontWeight.W_200)],
    alignment=ft.MainAxisAlignment.START,
)

# Friend 1 update
friend_1 = ft.Container(
    ft.Row(
        [
            ft.Image(
                src="https://www.allthingswild.co.uk/wp-content/uploads/2019/11/capy.jpg",
                border_radius=ft.border_radius.all(100),
                height=50,
                width=50,
            ),
            ft.Container(
                ft.Text(
                    "Co tam kapibary??",
                    size=15,
                ),
                padding=ft.padding.only(left=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    ),
    padding=ft.padding.only(left=15),
)

# Friend 2 update
# noinspection SpellCheckingInspection
friend_2 = ft.Container(
    ft.Row(
        [
            ft.Image(
                src="https://www.columbuszoo.org/sites/default/files/styles/uncropped_xl/public/assets/tours/Capybara"
                "%200360%20-%20Amanda%20Carberry%2C%20Columbus%20Zoo%20and%20Aquarium%20%281%29.jpg?itok=6K8he2dl",
                border_radius=ft.border_radius.all(100),
                height=50,
                width=50,
            ),
            ft.Container(
                ft.Text(
                    "Siema, jestem kapibarą",
                    size=15,
                ),
                padding=ft.padding.only(left=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    ),
    padding=ft.padding.only(left=15),
)

# Friend 3 update
# noinspection SpellCheckingInspection
friend_3 = ft.Container(
    ft.Row(
        [
            ft.Image(
                src="https://people.com/thmb/ovi1vkp7e_cTTPC5LglB_Ii83n0=/1500x0/filters:no_upscale():max_bytes(150000)"
                ":strip_icc():focal(149x0:151x2)/capybara-1-300-dbd2c51946de4b989723201dac1f20ff.jpg",
                border_radius=ft.border_radius.all(100),
                height=50,
                width=50,
            ),
            ft.Container(
                ft.Text(
                    "Jedzenieeee",
                    size=15,
                ),
                padding=ft.padding.only(left=10),
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=10,
    ),
    padding=ft.padding.only(left=15),
)

# Merge of friends updates
friends_updates = ft.Column(
    [
        friends_updates_title,
        friend_1,
        friend_2,
        friend_3,
    ]
)

# Achievements container
achievements_cont = ft.Container(
    ft.Row(
        [
            ft.Image(src="https://placehold.co/60x60/png"),
            ft.Image(src="https://placehold.co/60x60/png"),
        ]
    ),
    padding=ft.padding.all(13),
    border=ft.border.all(2, ft.colors.GREY_300),
    border_radius=ft.border_radius.all(20),
    bgcolor=ft.colors.GREY_100,
    alignment=ft.alignment.center,
    margin=10,
)

# User achievements
achievements = ft.Column(
    [
        ft.Text("Achievements", size=25, weight=ft.FontWeight.W_200),
        achievements_cont,
    ]
)

# Floating button to add a new post
new_post_btn = ft.FloatingActionButton(
    icon=ft.icons.ADD,
    on_click=new_post_onclick,
    bgcolor=ft.colors.RED_600,
)

social = View(name=FletNames.SOCIAL, route=f"/{FletNames.SOCIAL}")
social.add_component(DefaultComponents.STATISTICS_BAR.value)
social.add_component(
    Component(
        [
            ft.Column(
                [
                    usr_data,
                    ft.Divider(),
                    friends_updates,
                    ft.Divider(),
                    achievements,
                ],
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
            ),
            new_post_btn,
        ],
        "User data and image",
    )
)
social.add_component(DefaultComponents.NAVIGATION_BAR.value)
social.log()
