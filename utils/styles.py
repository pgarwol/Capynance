from enum import Enum
from utils.colors import Color
import flet as ft


class Style(Enum):
    ElevatedButton = {
        "color": Color.BLACK.value,
        "bgcolor": Color.ACCENT.value,
    }
    TextField = {
        "border": None,
        "border_width": 0,
        "filled": True,
        "cursor_color": Color.PRIMARY_LIGHTER.value,
        "label_style": ft.TextStyle(
            color=Color.PRIMARY_LIGHTER.value, weight=ft.FontWeight.W_400
        ),
    }
    IconButton = {
        "bgcolor": Color.PRIMARY_LIGHTER.value,
        "icon_color": Color.BLACK.value,
    }
    AppBar = {
        "bgcolor": Color.PRIMARY_DARKER.value,
        "color": Color.BLACK.value,
    }
    CupertinoSlidingSegmentedButton = {
        "thumb_color": Color.PRIMARY_DARKER.value,
        "bgcolor": Color.SECONDARY.value,
    }
    Dropdown = {
        "color": Color.WHITE.value,
    }
