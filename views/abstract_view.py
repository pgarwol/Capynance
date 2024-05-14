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

    @property
    @abstractmethod
    def var(self):
        pass

    @var.setter
    @abstractmethod
    def var(self, value):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def add_component(self):
        pass

    @abstractmethod
    def attach_page(self):
        pass
