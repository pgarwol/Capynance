from abc import ABC, abstractmethod


class AbstractView(ABC):
    """
    Summary:
    Abstract property for route in a view.

    Explanation:
    This abstract property must be implemented by subclasses to provide the route associated with a view.

    Args:
    - self

    Returns:
    - None
    """

    @property
    @abstractmethod
    def route(self):
        """
        Summary:
        Abstract property for route in a view.

        Explanation:
        This abstract property must be implemented by subclasses to provide the route associated with a view.

        Args:
        - self

        Returns:
        - None
        """
        pass

    @property
    @abstractmethod
    def components(self):
        """
        Summary:
        Abstract property for components in a view.

        Explanation:
        This abstract property must be implemented by subclasses to provide the components associated with a view.

        Args:
        - self

        Returns:
        - None
        """
        pass

    @abstractmethod
    def build(self):
        """
        Summary:
        Abstract method for building a view.

        Explanation:
        This abstract method must be implemented by subclasses to define the process of building a view.

        Args:
        - self

        Returns:
        - None
        """
        pass

    @abstractmethod
    def add_component(self):
        """
        Summary:
        Abstract method for adding a component to a view.

        Explanation:
        This abstract method must be implemented by subclasses to define the process of adding a component to a view.

        Args:
        - self

        Returns:
        - None
        """
        pass
