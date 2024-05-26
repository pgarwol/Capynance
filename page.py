from abc import ABC
from utils.enums import FletNames
import flet as ft


class Page(ABC):
    page = None

    @classmethod
    def set_page(cls, page: ft.Page):
        cls.page = page

    @classmethod
    def update(cls):
        if cls.page is not None:
            return cls.page.update()

    @classmethod
    def go(cls, route: str):
        if route is None:
            route = f"/{FletNames.HOME}"
        if cls.page is not None:
            return cls.page.go(route)

    @classmethod
    def toggle_dark_mode(cls, toggle_on: bool) -> None:
        """
        This class method toggles the dark mode of the application.

        It checks the value of the 'toggle_on' parameter. If it's True, it tries to set the theme mode of the page to
        DARK. If it's False, it tries to set the theme mode of the page to LIGHT. If an exception occurs while trying
        to set the theme mode, it prints an error message. After trying to set the theme mode, it updates the page.

        Args: toggle_on (bool): A boolean value indicating whether to turn on the dark mode. If True, the dark mode
        is turned on. If False, the dark mode is turned off.

        Returns:
            None
        """
        if toggle_on:
            try:
                cls.page.theme_mode = ft.ThemeMode.DARK
            except Exception as e:
                print('An error occurred while trying to set the theme mode to dark:', e)
        else:
            try:
                cls.page.theme_mode = ft.ThemeMode.LIGHT
            except Exception as e:
                print('An error occurred while trying to set the theme mode to light:', e)
        Page.update()
