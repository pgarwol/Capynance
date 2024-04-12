from components.component import Component
from views.abstract_view import AbstractView
from utils.exceptions import CapynanceException
import flet as ft


class View(AbstractView):
    """
    Summary:
    Class representing a concrete view.

    Explanation:
    This class extends AbstractView and defines a view with a route and components. It provides methods to build the view, add components, and generate a string representation.

    Args:
    - route: A string representing the route of the view.

    Returns:
    - None
    """

    def __init__(self, route: str):
        self._route = route
        self._components = []

    @property
    def route(self):
        """
        Summary:
        Property for accessing the route of a view.

        Explanation:
        This property allows access to the route associated with a view instance.

        Args:
        - self

        Returns:
        - The route of the view.
        """
        return self._route

    @property
    def components(self):
        """
        Summary:
        Property for accessing the components of a view.

        Explanation:
        This property allows access to the components associated with a view instance.

        Args:
        - self

        Returns:
        - The components of the view.
        """
        return self._components

    def build(self) -> ft.View:
        """
        Summary:
        Method for building a view.

        Explanation:
        This method constructs a view by unpacking components and creating a new ft.View instance with the route and unpacked components.

        Args:
        - self

        Returns:
        - An ft.View instance representing the constructed view.
        """
        unpacked_components = [
            item.content[0] for item in self.components if isinstance(item, Component)
        ]

        return ft.View(self.route, unpacked_components)

    def add_component(self, component: Component) -> None:
        """
        Summary:
        Method for adding a component to a view.

        Explanation:
        This method adds a component to the components list of the view instance. It raises a CapynanceException with the error type "invalid_components" if the provided component is not an instance of Component.

        Args:
        - component: The component to add to the view.

        Returns:
        - None
        Raises:
        - CapynanceException: If the provided component is not an instance of Component.
        """
        if isinstance(component, Component):
            self.components.append(component)
        else:
            raise CapynanceException("invalid_components")

    def __repr__(self):
        return f'View (\n\troute = "{self.route}",\n\tcomponents ({len(self.components)})\n)'
