from utils.lang import Lang
import copy
from components.component import Component
from views.abstract_view import AbstractView
from utils.exceptions import CapynanceException, Errors
from utils.enums import FletNames, DBFields
from io import StringIO
from page import Page
from pathlib import Path
from typing import Optional, List
import flet as ft


class View(AbstractView):
    _var = None

    def __init__(self, name: str, route: str):
        self._name = name
        self._route = route
        self._components = []
        self._var = {}
        self.refresh_language_contents = None
        self._lang = Lang(section=self.name)
        self.copy = copy.copy(self)
        View.instances.append(self)

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

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    def get_component(self, index: Optional[int] = 0) -> Component:
        """
        Retrieves a component at the specified index.

        Args:
            index (Optional[int]): The index of the component to retrieve. Defaults to 0.

        Returns:
            Component: The component at the specified index.
        """
        return self._components[index]

    def build(
        self,
        vertical_alignment: Optional[ft.MainAxisAlignment] = ft.MainAxisAlignment.START,
        horizontal_alignment: Optional[
            ft.CrossAxisAlignment
        ] = ft.CrossAxisAlignment.CENTER,
    ) -> ft.View:
        """
        Builds a view with the specified vertical and horizontal alignment.

        Args:
            vertical_alignment (Optional[ft.MainAxisAlignment]): The vertical alignment of the view.
                Defaults to MainAxisAlignment.START.
            horizontal_alignment (Optional[ft.CrossAxisAlignment]): The horizontal alignment of the view.
                Defaults to CrossAxisAlignment.CENTER.

        Returns:
            ft.View: The constructed view.
        """
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
        """
        Adds a component to the view.

        Args:
            component (Component): The component to add to the view.

        Returns:
            None

        Raises:
            CapynanceException: If the component is invalid.
        """
        if isinstance(component, Component):
            self.components.append(copy.copy(component))

        else:
            raise CapynanceException(Errors.INVALID_COMPONENT)

    def refresh_language_contents() -> None:
        """
        Refreshes the language contents for the view.

        Method implementation must be provided during instantiating View.
        """
        ...

    def attach_language_object(self, language: str) -> None:
        """
        Attaches a language object to the view.

        Args:
            language (str): The language to attach to the view.

        Returns:
            None
        """
        if isinstance(language, str):
            self.lang = Lang(section=self.name.lower(), language=language)

    def log(self) -> None:
        """
        Logs the view details and components to the build log file.
        """

        def append_build_log(content: str) -> None:
            with open(
                Path(DBFields.BUILD_LOG_PATH).resolve(), "a", encoding=DBFields.ENCODING
            ) as file:
                file.write(content)

        def list_all_controls(control_list: List[ft.Control]) -> str:
            buffer = StringIO()
            for i, control in enumerate(control_list):
                buffer.write("\t\t|---------------|----- " + f"{i}. {control}\n")
            return buffer.getvalue()

        def list_all_component_descriptions(self) -> str:
            buffer = StringIO()
            for i, component in enumerate(self._components):
                buffer.write(
                    "\t\t|----- "
                    + f"{i}. {component.description}\n{list_all_controls(component.content)}"
                )

            return buffer.getvalue()

        output = f"{self.name.capitalize()} | route = {self.route}\n\tcomponents:\n{list_all_component_descriptions(self)}\n\n"
        append_build_log(output)
