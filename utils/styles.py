from utils.enums import Colors
from enum import Enum
import flet as ft


class Style(Enum):
    ElevatedButton = {
        "color": Colors.BLACK,
        "bgcolor": Colors.ACCENT,
    }
    TextField = {
        "border": None,
        "border_width": 0,
        "filled": True,
        "cursor_color": Colors.PRIMARY_LIGHTER,
        "label_style": ft.TextStyle(
            color=Colors.PRIMARY_LIGHTER,
            weight=ft.FontWeight.W_400,
            font_family="RobotoSlab",
        ),
    }
    IconButton = {
        "bgcolor": Colors.PRIMARY_LIGHTER,
        "icon_color": Colors.BLACK,
    }
    AppBar = {
        "bgcolor": Colors.PRIMARY_DARKER,
        "color": Colors.BLACK,
    }
    Text = {"font_family": "RobotoSlab"}
    CupertinoSlidingSegmentedButton = {
        "thumb_color": Colors.PRIMARY_DARKER,
        "bgcolor": Colors.SECONDARY,
    }
    Dropdown = {
        "color": Colors.WHITE,
    }
