import logging
from abc import ABC
from utils.enums import FletNames
import flet as ft
from typing import Any


class Page(ABC):
    page = None
    observers = []

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
        Toggles the dark mode of the application.
        It should be called only from the ThemeManager class.

        Args:
            toggle_on (bool): If True, sets the theme mode to DARK. Otherwise, sets it to LIGHT.

        Returns:
            None
        """
        if cls.page is None:
            return

        try:
            cls.page.theme_mode = ft.ThemeMode.DARK if toggle_on else ft.ThemeMode.LIGHT
        except Exception as e:
            mode = "dark" if toggle_on else "light"
            logging.error(
                f"An error occurred while trying to set the theme mode to {mode}. {e}"
            )

        cls.update()

    @classmethod
    def show_snack_bar(cls, _: Any):
        return cls.page.show_snack_bar(_)
