from abc import ABC

from page import Page


class Session(ABC):

    @classmethod
    def set_logged_user(cls, logged_user):
        cls.logged_user = logged_user

    @classmethod
    def get_logged_user(cls):
        return cls.logged_user

    @classmethod
    def set_dark_mode(cls, dark_mode):
        cls.dark_mode = dark_mode

    @classmethod
    def set_language(cls, language):
        cls.language = language

    @classmethod
    def get_language(cls):
        return cls.language

    @classmethod
    def set_views(cls, views):
        cls.views = views

    @classmethod
    def translate_views_content(cls) -> None:
        """
        This function translates the content of all views to the current language.

        It iterates over all instances of the View class and changes the language of each view to the current language.
        It then updates the page to reflect these changes. If a view has a 'refresh_language_contents' method,
        it calls this method to refresh the language contents of the view.

        Returns:
            None
        """
        for view in cls.views:
            view.lang.change_language(cls.get_language())
            Page.update()
            if view.refresh_language_contents is not None:
                view.refresh_language_contents()

# Initialized after login
# Terminated after log out
# @TODO: Settings mechanics: dark mode, lang etc.
# Dark mode is already implemented in the page.py file. It can be change by calling the toggle_dark_mode method
