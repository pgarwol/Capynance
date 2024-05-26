import flet as ft
import flet_core

from components.component import Component
from page import Page
from session import Session
from utils.enums import FletNames, Colors
from views.view import View, ViewsInitialStates

header_size = 27
text_size = header_size - 10
cont_bg_color = '#122EC4B6'


def init_settings():
    """
    This function initializes the settings of the application based on the current language session.

    It checks the current language of the session. If the language is 'pl', it sets the value of the language
    dropdown to 'Polski'. If the language is 'en', it sets the value of the language dropdown to 'English'. If the
    language is neither 'pl' nor 'en', it prints an error message.

    Returns:
        None
    """
    if Session.get_language() == 'pl':
        dd_lang.value = 'Polski'
    elif Session.get_language() == 'en':
        dd_lang.value = 'English'
    else:
        print(f"Invalid language: {Session.get_language()}. Should be 'pl' or 'en'.")


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
    if e.data == 'true':
        Page.toggle_dark_mode(True)
    elif e.data == 'false':
        Page.toggle_dark_mode(False)
    else:
        raise ValueError(f"Invalid value: {e.data}. Should be 'true' or 'false'.")


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
        print(f'An error occurred: {e}')


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
    bug_desc.value = '\n\n\n'


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
    bug_desc.value = '\n\n\n'


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
    if lang == 'Polski':
        Session.set_language('pl')
    elif lang == 'English':
        Session.set_language('en')
    else:
        print(f"Invalid language: {lang}. Should be 'Polski' or 'English'.")
    Session.translate_views_content()


report_bug_dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text("Zgłoś błąd"),
    content=ft.Container(
        content=ft.Column(
            controls=[
                ft.Text('Opis błędu'),
                bug_desc := ft.TextField(
                    value='\n\n\n\n',
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
            style=ft.ButtonStyle(color=ft.colors.RED)
        ),
        ft.TextButton(
            text="Wyślij",
            on_click=confirm_report_bug_dialog,
            style=ft.ButtonStyle(color=Colors.PRIMARY_DARKER)
        ),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
)

cont_options = ft.Container(
    content=ft.Column(
        controls=[
            ft.Text('Opcje', size=header_size),
            ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Container(
                                ft.Text('Tryb ciemny', size=text_size),
                                padding=ft.Padding(top=0, left=10, right=0, bottom=0),
                            ),
                            ft.Container(ft.Switch(on_change=toggle_dark_mode)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                ft.Text('Język', size=text_size),
                                padding=ft.Padding(top=0, left=10, right=0, bottom=0),
                            ),
                            dd_lang := ft.Dropdown(
                                options=[
                                    ft.dropdown.Option('Polski'),
                                    ft.dropdown.Option('English'),
                                ],
                                width=150,
                                height=61,
                                on_change=change_language_dropdown,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ],
                spacing=0,
            )
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
            ft.Text('Konto', size=header_size),
            ft.Row([ft.TextButton(
                content=ft.Text('Zmień hasło', color='#22978C', size=text_size),
            )]),
            ft.Row([ft.TextButton(
                content=ft.Text('Usuń konto', color='#22978C', size=text_size),
            )]),
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
            ft.Text(value='Inne', size=header_size),
            ft.Row([ft.TextButton(
                content=ft.Text(value='Zgłoś błąd', color='#22978C', size=text_size),
                on_click=report_bug,
            )]),
            ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(value='Wersja aplikacji:', size=text_size),
                        padding=ft.Padding(top=0, left=10, right=0, bottom=0)
                    ),
                    ft.Container(ft.Text(value='1.0.0', size=text_size)),
                ],
                spacing=20
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
            ft.AppBar(
                title=ft.Text("Ustawienia aplikacji"),
                bgcolor=Colors.PRIMARY_DARKER
            )
        ],
        description="App bar showing the title of the page and allowing to navigate back to the home page.")
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
        description="Settings page content."
    )
)
ViewsInitialStates.set_settings_copy(settings)
settings.log()
