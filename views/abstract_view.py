from abc import ABC, abstractmethod


class AbstractView(ABC):
    lang = None
    instances = []

    @classmethod
    def set_lang(cls, lang):
        cls.lang = lang

    @classmethod
    def get_lang(cls):
        return cls.lang

    @classmethod
    def get_instances(cls):
        return cls.instances

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
    def refresh_language_contents(self):
        pass

    @abstractmethod
    def add_component(self):
        pass
