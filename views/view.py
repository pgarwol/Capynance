from components.component import Component
from views.abstract_view import AbstractView
from utils.exceptions import CapynanceException
from typing import Optional
from io import StringIO
import flet as ft


class View(AbstractView):
    _var = None

    def __init__(self, name: str, route: str):
        self._name = name
        self._route = route
        self._components = []
        self._var = {}

    @property
    def name(self):
        return self._name

    @property
    def route(self):
        return self._route

    @property
    def components(self):
        return self._components

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, value):
        self._var = value

    def get_component(self, index: Optional[int] = 0) -> Component:
        return self._components[index]

    def build(
        self,
        vertical_alignment: Optional[ft.MainAxisAlignment] = ft.MainAxisAlignment.START,
        horizontal_alignment: Optional[
            ft.CrossAxisAlignment
        ] = ft.CrossAxisAlignment.CENTER,
    ) -> ft.View:
        unpacked_components = [
            control
            for item in self.components
            if isinstance(item, Component)
            for control in item.content
            if isinstance(control, ft.Control)
        ]

        return ft.View(
            self.route,
            unpacked_components,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
        )

    def add_component(self, component: Component) -> None:
        if isinstance(component, Component):
            self.components.append(component)
        else:
            raise CapynanceException("invalid_components")

    def attach_page(self, page: ft.Page) -> None:
        if isinstance(page, ft.Page):
            self.var["page"] = page

    def __repr__(self):
        def list_all_component_descriptions(self) -> str:
            buffer = StringIO()
            for i, component in enumerate(self._components):
                buffer.write(
                    "\t\t"
                    + f"{i}. {component.description} | Controls: {component.content}"
                    + "\n"
                )
            buffer.write("\t]")

            return buffer.getvalue()

        return f'View (\n\tname = {self.name},\n\troute = "{self.route}",\n\tcomponents: [\n{list_all_component_descriptions(self)}\n)'
