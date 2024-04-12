from components.abstract_component import AbstractComponent
from typing import List, Optional
import flet as ft


class Component(AbstractComponent):
    """
    Summary:
    Class representing a concrete component.

    Explanation:
    This class extends AbstractComponent and defines a component with content, description, and page object properties. The content is a list of controls, description is an optional string, and page object is an optional Page instance.

    Args:
    - content: List of controls representing the content of the component.
    - description: Optional string describing the component (default is an empty string).
    - page_obj: Optional Page instance associated with the component (default is None).

    Returns:
    - None
    """

    def __init__(
        self,
        content: List[ft.Control],
        description: Optional[str] = "",
        page_obj: Optional[ft.Page] = None,
    ):
        self._content = content
        self._description = description
        self._page_obj = page_obj

    @property
    def content(self):
        """
        Summary:
        Property for accessing the content of a component.

        Explanation:
        This property allows access to the content of a component instance.

        Args:
        - self

        Returns:
        - The content of the component.
        """
        return self._content

    @property
    def description(self):
        """
        Summary:
        Property for accessing the description of a component.

        Explanation:
        This property allows access to the description of a component instance.

        Args:
        - self

        Returns:
        - The description of the component.
        """
        return self._description

    @property
    def page_obj(self):
        """
        Summary:
        Property for accessing the page object of a component.

        Explanation:
        This property allows access to the page object associated with a component instance.

        Args:
        - self

        Returns:
        - The page object of the component.
        """
        return self._page_obj
