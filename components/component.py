from utils.enums import Colors, FletNames
from utils.styles import Style
from utils.exceptions import CapynanceException
from components.abstract_component import AbstractComponent
import flet as ft
from enum import Enum
from typing import List


class Component(AbstractComponent):
    def __init__(
        self,
        content: List[ft.Control],
        description: str,
    ):
        super().__init__(content=content, description=description)

    @property
    def content(self):
        return self._content

    @property
    def description(self):
        return self._description

    def extend(self, control: ft.Control, index: int | str) -> None:
        """
        Extends the content of the component with the specified control at the given index.

        Args:
            control (ft.Control): The control to add to the component's content.
            index (int | str): The index at which to insert the control, or 'first'/'last' for specific positions.

        Returns:
            None

        Raises:
            CapynanceException: If the control is not a flet.Control, the index is unknown, or invalid.
        """
        if not isinstance(control, ft.Control):
            raise CapynanceException("control not flet.Control")

        if isinstance(index, str):
            index_mapping = {"first": 0, "last": -1}
            if index in index_mapping:
                i = index_mapping[index]
            else:
                raise CapynanceException("unknown index")
        elif isinstance(index, int):
            if index < -1 or index >= len(self.content):
                raise CapynanceException("index invalid")
            else:
                i = index
        else:
            raise CapynanceException("index invalid")

        self._content.insert(i, control)


class DefaultComponents(Enum):
    STATISTICS_BAR = Component(
        content=[
            ft.AppBar(
                title=ft.Text(FletNames.APP_NAME),
                center_title=True,
                actions=[ft.IconButton(icon=ft.icons.LOGOUT_OUTLINED)],
                **Style.AppBar.value
            ),
        ],
        description="Contains user stats located on the top.",
    )
    NAVIGATION_BAR = Component(
        content=[
            ft.BottomAppBar(
                ft.CupertinoSlidingSegmentedButton(
                    selected_index=3,
                    controls=[
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.QR_CODE_SCANNER,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.SHOPPING_CART_ROUNDED,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.CALENDAR_MONTH,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.HOME_ROUNDED,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.ATTACH_MONEY,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(name=ft.icons.PEOPLE, color=Colors.BLACK),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.SETTINGS_ROUNDED,
                                color=Colors.BLACK,
                            ),
                        ),
                    ],
                    **Style.CupertinoSlidingSegmentedButton.value
                )
            )
        ],
        description="Contains bottom navigation bar.",
    )
