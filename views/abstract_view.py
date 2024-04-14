from abc import ABC, abstractmethod


class AbstractView(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def route(self):
        pass

    @property
    @abstractmethod
    def components(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def add_component(self):
        pass
