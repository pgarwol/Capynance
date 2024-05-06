from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft

usr_img = ft.Image(src='https://via.placeholder.com/150')

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
        ft.ElevatedButton('Add friends', on_click=lambda _: print('Friends added!')),
    ],
    spacing=15
)

usr_data = ft.Row(
    [
        usr_img,
        usr_stats,
    ],
    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    vertical_alignment=ft.CrossAxisAlignment.START,
)

social = View(name="social", route="/social")
social.add_component(defaults["STATISTICS_BAR"])
social.add_component(Component([usr_data, ft.Divider()], "User data and image"))
social.add_component(defaults["NAVIGATION_BAR"])
