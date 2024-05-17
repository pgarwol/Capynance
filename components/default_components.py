from utils.colors import Color
from utils.styles import Style
from components.component import Component
import flet as ft

stats = Component(
    content=[
        ft.AppBar(
            title=ft.Text("Capynance."),
            center_title=True,
            actions=[ft.IconButton(icon=ft.icons.LOGOUT_OUTLINED)],
            **Style.AppBar.value
        ),
    ],
    description="Contains user stats located on the top.",
)
navigation = Component(
    content=[
        ft.BottomAppBar(
            ft.CupertinoSlidingSegmentedButton(
                selected_index=3,
                on_change=lambda _: print("siemka"),
                controls=[
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.QR_CODE_SCANNER,
                            color=Color.BLACK.value,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.SHOPPING_CART_ROUNDED,
                            color=Color.BLACK.value,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.CALENDAR_MONTH,
                            color=Color.BLACK.value,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.HOME_ROUNDED,
                            color=Color.BLACK.value,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.ATTACH_MONEY,
                            color=Color.BLACK.value,
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(name=ft.icons.PEOPLE, color=Color.BLACK.value),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.SETTINGS_ROUNDED,
                            color=Color.BLACK.value,
                        ),
                    ),
                ],
                **Style.CupertinoSlidingSegmentedButton.value
            )
        )
    ],
    description="Contains bottom navigation bar.",
)

defaults = {
    "STATISTICS_BAR": stats,
    "NAVIGATION_BAR": navigation,
}
