from components.component import Component
import flet as ft

stats = Component(
    content=[
        ft.AppBar(
            title=ft.Text("Capynance."),
            center_title=True,
            bgcolor=ft.colors.RED_700,
            color=ft.colors.GREY_100,
        ),
    ],
    description="Contains user stats located on the top.",
)
navigation = Component(
    content=[
        ft.BottomAppBar(
            ft.CupertinoSlidingSegmentedButton(
                selected_index=3,
                thumb_color=ft.colors.RED_700,
                bgcolor=ft.colors.GREY_100,
                on_change=lambda _: print("siemka"),
                controls=[
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.QR_CODE_SCANNER, color=ft.colors.RED_700
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.SHOPPING_CART_ROUNDED, color=ft.colors.RED_700
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.CALENDAR_MONTH, color=ft.colors.RED_700
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.HOME_ROUNDED, color=ft.colors.RED_700
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.ATTACH_MONEY, color=ft.colors.RED_700
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(name=ft.icons.PEOPLE, color=ft.colors.RED_700),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(
                            name=ft.icons.SETTINGS_ROUNDED, color=ft.colors.RED_700
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(0, 10),
                        content=ft.Icon(name=ft.icons.KEY, color=ft.colors.RED_700),
                    ),
                ],
            )
        )
    ],
    description="Contains bottom navigation bar.",
)

defaults = {
    "STATISTICS_BAR": stats,
    "NAVIGATION_BAR": navigation,
}
