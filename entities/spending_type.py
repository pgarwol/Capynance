import flet as ft
from abc import ABC


class SpendingType(ABC):
    instances = {}

    def __init__(self, search_name: str, full_name: str, icon: ft.Icon):
        self.search_name = search_name
        self.full_name = full_name
        self.icon = icon
        SpendingType.instances[self.search_name] = {
            "full_name": self.full_name,
            "icon": self.icon,
        }

    @classmethod
    def get_instance_by_name(cls, name: str):
        name_lowercased = name.lower()
        if name_lowercased in cls.instances:
            return SpendingType(name_lowercased, cls.instances[name_lowercased])

    @classmethod
    def get_instances(cls):
        return cls.instances


placeholder_icon = ft.Icon()
food = SpendingType("food", "Food", ft.Icon(ft.icons.FASTFOOD_OUTLINED))
housing = SpendingType(
    "housing",
    "Housing",
    ft.Icon(ft.icons.HOUSE_ROUNDED),
)
other_fees_and_bills = SpendingType(
    "other_fees_and_bills",
    "Other Fees and Bills",
    ft.Icon(ft.icons.ELECTRICAL_SERVICES),
)
health_hygiene_and_chemicals = SpendingType(
    "health_hygiene_and_chemicals",
    "Health, Hygiene, and Chemicals",
    ft.Icon(ft.icons.WASH),
)
clothing = SpendingType("clothing", "Clothing", ft.Icon(ft.icons.SHOPPING_BAG_ROUNDED))
leisure = SpendingType(
    "leisure",
    "Leisure",
    ft.Icon(ft.icons.FAVORITE_OUTLINED),
)
transport = SpendingType(
    "transport",
    "Transport",
    ft.Icon(ft.icons.DIRECTIONS_BUS_ROUNDED),
)
subscriptions = SpendingType(
    "subscriptions",
    "Subscriptions",
    ft.Icon(ft.icons.EVENT_REPEAT_OUTLINED),
)
other_expenses = SpendingType(
    "other_expenses", "Other Expenses", ft.Icon(ft.icons.QUESTION_MARK_OUTLINED)
)
