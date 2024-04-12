from views.main_screen import main_screen
import flet as ft


def main(page: ft.Page):
    page.title = "Capynance"

    def route_change(route):
        page.views.clear()

        page.views.append(main_screen.build())
        # if page.route == main_screen.route:
        #     # page.views.append(main_screen.build())
        #     pass
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
