from components.component import Component
import flet as ft

stats = Component(
    content=[
        ft.AppBar(
            title=ft.Text("Tutaj będą statystyki gracza, wiesz co jest pięć"),
            bgcolor=ft.colors.SURFACE_VARIANT,
        ),
    ],
    description="Contains user stats located on the top.",
)
navigation = Component(
    content=[
        ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.EXPLORE, label="kompasik"),
                ft.NavigationDestination(icon=ft.icons.COMMUTE, label="ałtko"),
                ft.NavigationDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="zakładeczka",
                ),
            ]
        )
    ],
    description="Contains bottom navigation bar.",
)

defaults = {
    "STATS": stats,
    "NAVIGATION": navigation,
}
