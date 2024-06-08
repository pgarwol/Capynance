import time
import logging

import flet as ft
import flet_core

from components.component import Component, DefaultComponents
from page import Page
from session import Session
from utils import services
from utils.enums import FletNames, Colors
from utils.sync_manager import SyncManager
from utils.theme_manager import ThemeManager
from views.view import View, ViewsInitialStates

header_size = 27
text_size = header_size - 10
cont_bg_color = "#122EC4B6"
txt_snackbar_account_deleted = ft.Text("Konto zostało usunięte pomyślnie")
txt_snackbar_password_changed = ft.Text("Hasło zostało zmienione pomyślnie")
txt_error_incompatible_passwords = "Nowe hasła nie są takie same"
txt_error_incorrect_password = "Niepoprawne hasło"


class UserData:
    """
    A class used to represent User Data.
    """

    @classmethod
    def set_login(cls, login: str):
        """
        Class method to set the login attribute of the UserData class.

        Args:
            login (str): The login of the user.

        Returns:
            None
        """
        cls.login = login


def refresh_labels() -> None:
    """
    This function changes view's texts based on the current language.

    :return: None
    """
    txt_options.value = settings.lang['options']
    txt_dark_mode.value = settings.lang['dark_mode']
    txt_language.value = settings.lang['language']
    txt_account.value = settings.lang['account']
    btn_change_password.content.value = settings.lang['change_password']
    btn_delete_account.content.value = settings.lang['delete_account']
    txt_misc.value = settings.lang['misc']
    btn_report_bug.content.value = settings.lang['report_bug']
    txt_app_version.value = settings.lang['app_version']

    txt_change_password.value = settings.lang['change_password']
    txt_old_password.value = settings.lang['old_password']
    txt_new_password.value = settings.lang['new_password']
    txt_confirm_password.value = settings.lang['confirm_password']
    change_password_dialog.actions[0].text = settings.lang['cancel']
    change_password_dialog.actions[1].text = settings.lang['change']

    txt_delete_account_title.value = settings.lang['delete_account']
    txt_delete_account_warning.value = settings.lang['delete_account_warning']
    txt_delete_account_password.value = settings.lang['delete_account_password']
    delete_account_dialog.actions[0].text = settings.lang['delete_account']
    delete_account_dialog.actions[1].text = settings.lang['cancel']

    txt_report_bug_title.value = settings.lang['report_bug']
    txt_report_bug_desc.value = settings.lang['report_bug_description']
    report_bug_dialog.actions[0].text = settings.lang['cancel']
    report_bug_dialog.actions[1].text = settings.lang['send']

    global txt_error_incompatible_passwords, txt_error_incorrect_password
    txt_snackbar_account_deleted.value = settings.lang['account_deleted']
    txt_snackbar_password_changed.value = settings.lang['password_changed']
    app_bar_settings.title.value = settings.lang['app_settings']
    txt_error_incompatible_passwords = settings.lang['error_incompatible_passwords']
    txt_error_incorrect_password = settings.lang['error_incorrect_password']


def init_settings(login: str, dark_mode_on: bool) -> None:
    """
    Initializes the settings for the user session.

    This function sets the language and theme mode for the session based on the provided arguments. It also creates a
    LocalThemeManager instance with the current theme mode and adds it as an observer to the ThemeManager.

    Args:
        login (str): The login of the user.
        dark_mode_on (bool): A boolean indicating whether the dark mode is on.

    Returns:
        None
    """
    # Set the language for the session based on the current language setting
    if Session.get_language() == "pl":
        dd_lang.value = "Polski"
    elif Session.get_language() == "en":
        dd_lang.value = "English"
    else:
        logging.error(
            f"Invalid language: {Session.get_language()}. Should be 'pl' or 'en'."
        )

    # Set the login for the user data
    UserData.set_login(login)

    # Set the value of the theme mode switch based on the dark_mode_on argument
    theme_mode_switch.value = dark_mode_on

    # Create a LocalThemeManager instance with the current theme mode
    theme_info = LocalThemeManager(ThemeManager.theme_mode)
    # Add the LocalThemeManager instance as an observer to the ThemeManager
    ThemeManager.remove_observer(theme_info)
    ThemeManager.add_observer(theme_info)

    # Set the language for the session based on the current language setting
    refresh_labels()


def toggle_dark_mode(e: flet_core.control_event.Event) -> None:
    """
    This function toggles the dark mode of the application based on the event data.

    It checks the data of the event. If the data is 'true', it enables the dark mode.
    If the data is 'false', it disables the dark mode.
    If the data is neither 'true' nor 'false', it raises a ValueError.

    Args:
        e (flet_core.control_event.Event): The event that triggered the function. The data of the event should be
        'true' or 'false'.

    Raises:
        ValueError: If the data of the event is not 'true' or 'false'.

    Returns:
        None
    """
    if e.data == "true":
        ThemeManager.toggle_dark_mode(True)
    elif e.data == "false":
        ThemeManager.toggle_dark_mode(False)
    else:
        raise ValueError(f"Invalid value: {e.data}. Should be 'true' or 'false'.")


theme_mode_switch = ft.Switch(on_change=toggle_dark_mode)


class LocalThemeManager:
    """
    A class used to represent a Local Theme Manager. It helps to manage the theme of the application.
    """

    def __init__(self, theme: ft.ThemeMode):
        """
        Initializes the LocalThemeManager with the provided theme.

        Args:
            theme (ft.ThemeMode): The theme to be remembered.

        Returns:
            None
        """
        self.theme_mode = theme

    def on_change_theme(self, theme: ft.ThemeMode) -> None:
        """
        This method changes the switch position based on the theme mode.
        :param theme: The theme mode to be set.
        :return: None
        """
        self.theme_mode = theme
        if theme == ft.ThemeMode.DARK:
            theme_mode_switch.value = True
        elif theme == ft.ThemeMode.LIGHT:
            theme_mode_switch.value = False
        else:
            theme_mode_switch.value = False
            logging.error(
                f"Invalid theme mode: {theme}. Should be DARK or LIGHT. Setting switch to default off "
                f"position."
            )


def report_bug(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the reporting of bugs in the application.

    It sets the dialog of the page to the 'report_bug_dialog' and opens it.
    It then updates the page to reflect these changes.
    If an exception occurs during this process, it prints an error message.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    try:
        e.page.dialog = report_bug_dialog
        report_bug_dialog.open = True
        e.page.update()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def discard_report_bug_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the discarding of the bug report dialog.

    It closes the dialog of the page and updates the page to reflect this change.
    It also resets the value of the bug description to its initial state.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    e.page.dialog.open = False
    e.page.update()
    bug_desc.value = "\n\n\n"


def confirm_report_bug_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the confirmation of the bug report dialog.

    It closes the dialog of the page and updates the page to reflect this change.
    It then prints the reported bug description and resets the value of the bug description to its initial state.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    e.page.dialog.open = False
    e.page.update()
    print(f'A bug has been reported: "{bug_desc.value}"')
    bug_desc.value = "\n\n\n"


def change_language_dropdown(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function changes the language of the application based on the selected dropdown value.

    It checks the value of the dropdown. If the value is 'Polski', it sets the language of the session to 'pl'.
    If the value is 'English', it sets the language of the session to 'en'.
    If the value is neither 'Polski' nor 'English', it prints an error message.
    After setting the language, it translates the content of all views to the current language.

    Args: e (flet_core.control_event.ControlEvent): The event that triggered the function. The value of the dropdown
    is obtained from the control of the event.

    Returns:
        None
    """
    lang = e.control.value
    logged_user = Session.get_logged_user()
    if lang == "Polski":
        Session.set_language("pl")
        logged_user.settings["language"] = "pl"
    elif lang == "English":
        Session.set_language("en")
        logged_user.settings["language"] = "en"
    else:
        logging.error(f"Invalid language: {lang}. Should be 'Polski' or 'English'.")
    SyncManager.sync_settings()
    Session.translate_views_content()


def change_password(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the process of changing the password.

    It sets the dialog of the page to the 'change_password_dialog' and opens it.
    It then updates the page to reflect these changes.
    If an exception occurs during this process, it prints an error message.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    try:
        e.page.dialog = change_password_dialog
        change_password_dialog.open = True
        e.page.update()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def discard_change_password_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the discarding of the change password dialog.

    It closes the dialog of the page and updates the page to reflect this change.
    It also resets the values of the password fields to their initial state.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    e.page.dialog.open = False
    e.page.update()
    clear_change_password_dialog()


def confirm_change_password_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the confirmation of the change password dialog.

    It checks if the old password is valid and if the new passwords match.
    If the checks pass, it changes the password, closes the dialog, and shows a success message.
    If the checks fail, it shows an error message.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    check_result = services.is_login_valid(UserData.login, tf_old_password.value)
    remove_password_error(change_password_dialog_content, content_limit_with_error=7)
    if check_result[0]:
        if (
            tf_new_password.value == tf_confirm_password.value
            and tf_new_password.value != ""
        ):
            services.change_password(
                UserData.login, tf_old_password.value, tf_new_password.value
            )
            e.page.dialog.open = False
            Page.page.snack_bar = ft.SnackBar(
                txt_snackbar_password_changed
            )
            Page.page.snack_bar.open = True
            clear_change_password_dialog()  # Includes page update
        else:
            throw_password_error(
                e,
                txt_error_incompatible_passwords,
                content=change_password_dialog_content,
                content_limit=6,
            )
    else:
        throw_password_error(
            e,
            txt_error_incorrect_password,
            content=change_password_dialog_content,
            content_limit=6,
        )


def throw_password_error(
    e: flet_core.control_event.ControlEvent,
    error_message: str,
    content: list[flet_core],
    content_limit: int,
) -> None:
    """
    This function handles the display of password errors.

    It adds an error message to the dialog content if it's not already displayed and updates the page.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.
        error_message (str): The error message to be displayed.
        content (list[flet_core]): The content of the dialog.
        content_limit (int): The limit of the content list. It helps to check if the error message is already displayed.
    It should indicate the length of the content list before the error message is added.

    Returns:
        None
    """
    if len(content) == content_limit:  # Check if the error message is already displayed
        content.append(ft.Text(error_message, color="red"))
    e.page.update()


def clear_change_password_dialog() -> None:
    """
    This function resets the values of the password fields to their initial state.

    It clears the values of the old password, new password, and confirm password fields.
    It also removes the error message if it's displayed.

    Returns:
        None
    """
    tf_old_password.value = ""
    tf_new_password.value = ""
    tf_confirm_password.value = ""
    remove_password_error(change_password_dialog_content, content_limit_with_error=7)


def remove_password_error(
    content: list[flet_core], content_limit_with_error: int
) -> None:
    """
    This function removes the password error message.

    It removes the error message from the dialog content if it's displayed and updates the page.

    Args:
        content (list[flet_core]): The content of the dialog.
        content_limit_with_error (int): The limit of the content list with the error message. It indicates the length
    of the content list before the error message is added.

    Returns:
        None
    """
    if len(content) == content_limit_with_error:
        content.pop()  # Remove the error message if it's displayed
    Page.update()


def delete_account(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the process of deleting the account.

    It shows a confirmation dialog to the user. If the user confirms the deletion, it deletes the account.
    If the user cancels the deletion, it closes the dialog and shows a success message.
    If an exception occurs during this process, it prints an error message.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    try:
        e.page.dialog = delete_account_dialog
        delete_account_dialog.open = True
        e.page.update()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def confirm_delete_account_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the confirmation of the account deletion dialog.

    It first clears the last error message, if any. Then, it checks if the password entered by the user is correct.
    If the password is incorrect, it shows an error message and returns.

    If the password is correct, it logs out the user and redirects them to the login page. It then deletes the account
    by calling the services.delete_account method and closes the dialog.

    Finally, it shows a success message to the user.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """

    # Clear last error message and set up variables.
    remove_password_error(delete_account_dialog_content, content_limit_with_error=4)
    password = tf_delete_acc_password.value
    login = UserData.login

    # Check if the password is correct. If not, show an error message and return.
    if not services.is_login_valid(login, password)[0]:
        throw_password_error(
            e,
            error_message=txt_error_incorrect_password,
            content=delete_account_dialog_content,
            content_limit=3,
        )
        return

    # Log out user and redirect to the login page
    DefaultComponents.NAVIGATION_BAR.value.content[0].selected_index = (
        DefaultComponents.DEFAULT_MENU_SELECTION.value
    )
    View.reset_views()
    Page.update()
    time.sleep(1)

    # Delete the account by calling the services.delete_account method.
    services.delete_account(login, password)
    e.page.dialog.open = False

    # Show a success message
    Page.page.snack_bar = ft.SnackBar(
        txt_snackbar_account_deleted
    )
    Page.page.snack_bar.open = True
    Page.update()


def discard_delete_account_dialog(e: flet_core.control_event.ControlEvent) -> None:
    """
    This function handles the discarding of the account deletion dialog.

    It closes the dialog of the page and updates the page to reflect this change.
    It also resets the value of the delete account password field to its initial state.

    Args:
        e (flet_core.control_event.ControlEvent): The event that triggered the function.

    Returns:
        None
    """
    e.page.dialog.open = False
    e.page.update()
    tf_delete_acc_password.value = ""
    remove_password_error(delete_account_dialog_content, content_limit_with_error=4)


# Bug report dialog
report_bug_dialog = ft.AlertDialog(
    True,
    txt_report_bug_title :=ft.Text("Zgłoś błąd"),
    content=ft.Container(
        content=ft.Column(
            controls=[
                txt_report_bug_desc := ft.Text("Opis błędu"),
                bug_desc := ft.TextField(
                    value="\n\n\n\n",
                    multiline=True,
                    height=150,
                ),
            ]
        ),
        height=200,
    ),
    actions=[
        ft.TextButton(
            text="Anuluj",
            on_click=discard_report_bug_dialog,
            style=ft.ButtonStyle(color=ft.colors.RED),
        ),
        ft.TextButton(
            text="Wyślij",
            on_click=confirm_report_bug_dialog,
            style=ft.ButtonStyle(color=Colors.PRIMARY_DARKER),
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

# Change password dialog
change_password_dialog = ft.AlertDialog(
    True,
    txt_change_password := ft.Text("Zmień hasło"),
    content=ft.Container(
        content=ft.Column(
            change_password_dialog_content := [
                txt_old_password := ft.Text("Stare hasło"),
                tf_old_password := ft.TextField(
                    password=True,
                    can_reveal_password=True,
                ),
                txt_new_password := ft.Text("Nowe hasło"),
                tf_new_password := ft.TextField(
                    password=True,
                    can_reveal_password=True,
                ),
                txt_confirm_password := ft.Text("Potwierdź nowe hasło"),
                tf_confirm_password := ft.TextField(
                    password=True,
                    can_reveal_password=True,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
        ),
        height=320,
    ),
    actions=[
        ft.TextButton(
            text="Anuluj",
            on_click=discard_change_password_dialog,
            style=ft.ButtonStyle(color=ft.colors.RED),
        ),
        ft.TextButton(
            text="Zmień",
            on_click=confirm_change_password_dialog,
            style=ft.ButtonStyle(color=Colors.PRIMARY_DARKER),
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

# Delete account dialog
delete_account_dialog = ft.AlertDialog(
    True,
    txt_delete_account_title := ft.Text("Usuń konto"),
    content=ft.Container(
        content=ft.Column(
            delete_account_dialog_content := [
                txt_delete_account_warning := ft.Text(
                    value="Uwaga! Ta akcja jest nieodwracalna.",
                    color="red"
                ),
                txt_delete_account_password := ft.Text("W celu usunięcia, podaj hasło:"),
                tf_delete_acc_password := ft.TextField(
                    password=True,
                    can_reveal_password=True,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN,
        ),
        height=160,
    ),
    actions=[
        ft.TextButton(
            text="Usuń konto",
            on_click=confirm_delete_account_dialog,
            style=ft.ButtonStyle(color=ft.colors.RED),
        ),
        ft.TextButton(
            text="Anuluj",
            on_click=discard_delete_account_dialog,
            style=ft.ButtonStyle(color=Colors.PRIMARY_DARKER),
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

cont_options = ft.Container(
    content=ft.Column(
        controls=[
            txt_options := ft.Text("Opcje", size=header_size),
            ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Container(
                                txt_dark_mode := ft.Text("Tryb ciemny", size=text_size),
                                padding=ft.Padding(top=0, left=10, right=0, bottom=0),
                            ),
                            ft.Container(theme_mode_switch),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                txt_language := ft.Text("Język", size=text_size),
                                padding=ft.Padding(top=0, left=10, right=0, bottom=0),
                            ),
                            dd_lang := ft.Dropdown(
                                options=[
                                    ft.dropdown.Option("Polski"),
                                    ft.dropdown.Option("English"),
                                ],
                                width=150,
                                height=61,
                                on_change=change_language_dropdown,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=0,
            ),
        ],
    ),
    bgcolor=cont_bg_color,
    margin=10,
    padding=10,
    border_radius=10,
)

cont_account = ft.Container(
    content=ft.Column(
        controls=[
            txt_account := ft.Text("Konto", size=header_size),
            ft.Row(
                [
                    btn_change_password := ft.TextButton(
                        content=ft.Text("Zmień hasło", color="#22978C", size=text_size),
                        on_click=change_password,
                    )
                ]
            ),
            ft.Row(
                [
                    btn_delete_account := ft.TextButton(
                        content=ft.Text("Usuń konto", color="#22978C", size=text_size),
                        on_click=delete_account,
                    )
                ]
            ),
        ],
        spacing=0,
    ),
    bgcolor=cont_bg_color,
    margin=10,
    padding=10,
    border_radius=10,
)

cont_misc = ft.Container(
    content=ft.Column(
        controls=[
            txt_misc := ft.Text(value="Inne", size=header_size),
            ft.Row(
                [
                    btn_report_bug := ft.TextButton(
                        content=ft.Text(
                            value="Zgłoś błąd", color="#22978C", size=text_size
                        ),
                        on_click=report_bug,
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        txt_app_version := ft.Text(value="Wersja aplikacji:", size=text_size),
                        padding=ft.Padding(top=0, left=10, right=0, bottom=0),
                    ),
                    ft.Container(ft.Text(value="1.0.0", size=text_size)),
                ],
                spacing=20,
            ),
        ],
        spacing=0,
    ),
    bgcolor=cont_bg_color,
    margin=10,
    padding=10,
    border_radius=10,
)

settings = View(name=FletNames.SETTINGS, route=f"/{FletNames.SETTINGS}")
settings.add_component(
    Component(
        content=[
            app_bar_settings := ft.AppBar(
                title=ft.Text("Ustawienia aplikacji"), bgcolor=Colors.PRIMARY_DARKER
            )
        ],
        description="App bar showing the title of the page and allowing to navigate back to the home page.",
    )
)
settings.add_component(
    Component(
        content=[
            ft.Column(
                [
                    cont_options,
                    cont_account,
                    cont_misc,
                ],
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
            )
        ],
        description="Settings page content.",
    )
)

settings.refresh_language_contents = refresh_labels
ViewsInitialStates.set_settings_copy(settings)
settings.log()
