from views.main_screen import main_screen
from views.shop import shop
import flet as ft
from abc import ABC
from components.component import Component


def main(page: ft.Page):
    page.title = "Capynance"
    # To avoid problems with ft.Page variable scope
    main_screen.get_component(0).add_control(
        ft.ElevatedButton(
            "Wejdź se do sklepa tego typu", on_click=lambda _: page.go("/shop")
        ),
        index="last",
    )

    def route_change(route):
        page.views.clear()
        page.views.append(main_screen.build())
        if page.route == shop.route:
            page.views.append(shop.build())
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
