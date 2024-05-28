from page import Page
from session import Session
from utils import services


class SyncManager:
    """
    Class responsible for synchronizing the user data with the database.
    """

    @classmethod
    def save_data(cls, filename: str) -> None:
        """
        Save specific data to the database.

        :param: None
        :return:
        """
        user = Session.get_logged_user()
        services.save_file_data(filename, user)

    @classmethod
    def set_init_functions(cls, init_calendar: callable, init_finances: callable,
                           init_stats: callable, init_scan: callable, init_home: callable) -> None:
        """
        Sets the initialization functions for the views. They will be used to synchronize the data with the database.

        :param init_calendar: Initialization function for the calendar view.
        :param init_finances: Initialization function for the finances view.
        :param init_stats: Initialization function for the statistics view.
        :param init_scan: Initialization function for the scan view.
        :param init_home: Initialization function for the home view.
        :return: None
        """
        cls.init_calendar = init_calendar
        cls.init_finances = init_finances
        cls.init_stats = init_stats
        cls.init_scan = init_scan
        cls.init_home = init_home

    @classmethod
    def set_db_fields(cls, db_fields) -> None:
        """
        Sets the database fields for the user data.

        :param db_fields: The database fields for the user data.
        :return: None
        """
        cls.db_fields = db_fields

    @classmethod
    def sync_calendar(cls) -> None:
        """
        Synchronizes the calendar data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.CALENDAR)
        cls.init_calendar()
        Page.update()

    @classmethod
    def sync_finances(cls) -> None:
        """
        Synchronizes the finances data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.FINANCES)
        cls.init_finances()
        Page.update()

    @classmethod
    def sync_stats(cls) -> None:
        """
        Synchronizes the statistics data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.STATS)
        cls.init_stats()
        Page.update()

    @classmethod
    def sync_scan(cls) -> None:
        """
        Synchronizes the scan data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.MANUAL_SPENDING)
        cls.init_scan()
        Page.update()

    @classmethod
    def sync_settings(cls) -> None:
        """
        Synchronizes the settings data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.SETTINGS)
        Page.update()

    @classmethod
    def sync_shop(cls) -> None:
        """
        Synchronizes the shop data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.SHOP)
        Page.update()

    @classmethod
    def sync_profile(cls) -> None:
        """
        Synchronizes the profile data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.PROFILE)
        Page.update()

    @classmethod
    def sync_manual_spending(cls) -> None:
        """
        Synchronizes the manual spending data with the database

        :param: None
        :return:
        """
        cls.save_data(cls.db_fields.MANUAL_SPENDING)
        cls.init_home()
        Page.update()
