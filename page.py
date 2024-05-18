from abc import ABC
from utils.enums import FletNames
import flet as ft


class Page(ABC):

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
