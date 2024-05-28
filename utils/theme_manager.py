import flet as ft

from page import Page


class ThemeManager:
    """
    The ThemeManager class is responsible for managing the theme of the application.
    It uses the Observer design pattern to notify all observers when the theme changes.
    """

    # A list of observers that will be notified when the theme changes.
    observers = []

    @classmethod
    def add_observer(cls, observer):
        """
        Adds an observer to the list of observers. The observer must have an 'on_change_theme' method.

        Args:
            observer (object): The observer to be added. Must have an 'on_change_theme' method.

        Raises:
            TypeError: If the observer does not have an 'on_change_theme' method.
        """
        if not hasattr(observer, 'on_change_theme') or not callable(getattr(observer, 'on_change_theme')):
            raise TypeError('Observer must have an "on_change_theme" method')

        cls.observers.append(observer)

    @classmethod
    def remove_observer(cls, observer):
        """
        Removes an observer from the list of observers.

        Args:
            observer (object): The observer to be removed.
        """
        if observer in cls.observers:
            cls.observers.remove(observer)

    @classmethod
    def __notify(cls, current_theme: ft.ThemeMode):
        """
        Notifies all observers about the theme change by calling their 'on_change_theme' method.

        Args:
            current_theme (ft.ThemeMode): The current theme of the application.
        """
        for observer in cls.observers:
            observer.on_change_theme(current_theme)

    @classmethod
    def toggle_dark_mode(cls, toggle_on: bool) -> None:
        """
        Toggles the dark mode/light mode of the application and notifies all observers about the theme change.

        Args:
            toggle_on (bool): If True, sets the theme mode to DARK. Otherwise, sets it to LIGHT.
        """
        Page.toggle_dark_mode(toggle_on)
        cls.theme_mode = ft.ThemeMode.DARK if toggle_on else ft.ThemeMode.LIGHT
        cls.__notify(cls.theme_mode)
