from abc import ABC, abstractmethod


class AbstractComponent(ABC):
    """
    Summary:
    Abstract base class for components.

    Explanation:
    This class defines abstract properties for content, description, and page object. Subclasses must implement these properties to define specific behavior for different types of components.

    Args:
    - self

    Returns:
    - None

    Examples:
    This class is not meant to be instantiated directly but serves as a blueprint for creating concrete component classes.
    """

    @property
    @abstractmethod
    def content(self):
        """
        Summary:
        Abstract property for content.

        Explanation:
        This abstract property must be implemented by subclasses to provide the content of the component.

        Args:
        - self

        Returns:
        - None
        """

        pass

    @property
    @abstractmethod
    def description(self):
        """
        Summary:
        Abstract property for description.

        Explanation:
        This abstract property must be implemented by subclasses to provide the description of the component.

        Args:
        - self

        Returns:
        - None
        """
        pass

    @property
    @abstractmethod
    def page_obj(self):
        """
        Summary:
        Abstract property for page object.

        Explanation:
        This abstract property must be implemented by subclasses to provide the page object associated with the component.

        Args:
        - self

        Returns:
        - None
        """
        pass
