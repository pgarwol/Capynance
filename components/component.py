from components.abstract_component import AbstractComponent
from utils.exceptions import CapynanceException
from typing import List, Optional
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

    def add_control(self, control: ft.Control, index: int | str) -> None:
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
