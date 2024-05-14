from abc import ABC, abstractmethod


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

    @abstractmethod
    def extend(self):
        pass
