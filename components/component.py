from utils.exceptions import CapynanceException
from components.abstract_component import AbstractComponent
from typing import List
import flet as ft


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
