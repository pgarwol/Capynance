from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict
import flet as ft


class AbstractComponent(ABC):

    def __init__(self, content, description):
        self._content = content
        self._description = description

    @property
    @abstractmethod
    def content(self):

        pass

    @property
    @abstractmethod
    def description(self):
        pass
