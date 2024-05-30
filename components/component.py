from utils.enums import Colors
import copy
from utils.styles import Style
from utils.exceptions import CapynanceException
from components.abstract_component import AbstractComponent
import flet as ft
from enum import Enum
from typing import List
import utils.services as services
from session import Session
import copy
from page import Page
from utils.enums import FletNames, DBFields
from product import read_product_from_db


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


stats_var = {}
default_equipped = "https://lh3.googleusercontent.com/pw/AP1GczP22h9zKEFj7hcIiX-9gfwtRm-W8KPJSP-oYdHEt-0pvgZPy0QOduH8KnGHpC9UFQHT2O_m3jTDisvzGqPEDiWxlC6AFGXdoeFzUYenecjZtIn38Xy-7MbRwAD7tN-iH_OM2iw13cy_YdzpixrzK0E=w725-h857-s-no-gm?authuser=0"
exp_img = "https://static.wikia.nocookie.net/minecraft/images/0/0a/ExperienceOrb.gif/revision/latest/smart/width/371/height/332?cb=20190907041203"
coin_img = "https://lh3.googleusercontent.com/pw/AP1GczNFNx7f733rhrtzgyaB22YjoMxkNio2F4u9eMEW4milxdp3RU82RsAF2p0S5DR-rVfZYhqXtukjwKk0dF7O_MIEsFm0-Wfvdts8FRRj_VTq7oizSUZLhsKmDBv7SLm3yo45gT9rWtRBCMKrPz5z_CI=w857-h857-s-no-gm?authuser=0"


# Stats
life_hearts = None

hat_equipped = None
color_equipped = None
shirt_equipped = None

capycoins = None
lvl = None
exp = None


image_width = 75
image_height = (71 * image_width) / 60


class DefaultComponents(Enum):
    DEFAULT_MENU_SELECTION = 3

    STATISTICS_BAR = Component(
        content=[
            ft.AppBar(
                title=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                leading=ft.Container(
                    ft.Row(controls=[], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    alignment=ft.alignment.center,
                    padding=ft.Padding(5, 0, 5, 0),
                    margin=ft.Margin(0, 0, 0, 0),
                    width=250,
                    height=85,
                ),
                actions=[
                    ft.IconButton(
                        icon=ft.icons.LOGOUT_OUTLINED, icon_color=Colors.BLACK
                    ),
                ],
                bgcolor=Colors.PRIMARY_DARKER,
                center_title=True,
                leading_width=50,
                toolbar_height=100,
            ),
        ],
        description="Contains user stats located on the top.",
    )

    NAVIGATION_BAR = Component(
        content=[
            ft.BottomAppBar(
                ft.CupertinoSlidingSegmentedButton(
                    selected_index=2,
                    controls=[
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.QR_CODE_SCANNER,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.SHOPPING_CART_ROUNDED,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.HOME_ROUNDED,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.CALENDAR_MONTH,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.ATTACH_MONEY,
                                color=Colors.BLACK,
                            ),
                        ),
                    ],
                    **Style.CupertinoSlidingSegmentedButton.value,
                )
            )
        ],
        description="Contains bottom navigation bar.",
    )


import math


def create_equipped_images(hat_img, color_img, shirt_img):
    controls = []

    if color_img:
        controls.append(
            ft.Image(
                src=color_img,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    if hat_img:
        controls.append(
            ft.Image(
                src=hat_img,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    if shirt_img:
        controls.append(
            ft.Image(
                src=shirt_img,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    if not controls:
        controls.append(
            ft.Image(
                src=DBFields.DEFAULT_SKIN,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    return ft.Container(
        content=ft.Stack(controls=controls, width=image_width, height=image_height),
        alignment=ft.alignment.center,
        bgcolor=Colors.SECONDARY,
        border_radius=ft.border_radius.all(8),
        width=82,
        height=82,
        border=ft.border.all(2, Colors.ACCENT),
        margin=ft.margin.Margin(10, 0, 5, 0),
        padding=ft.padding.all(3),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.colors.BLACK54,
            offset=ft.Offset(0, 0),
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.Alignment(0.8, 1),
            colors=[
                "0xff1f005c",
                "0xff5b0060",
                "0xff870160",
                "0xffac255e",
                "0xffca485c",
                "0xffe16b5c",
                "0xfff39060",
                "0xffffb56b",
            ],
            tile_mode=ft.GradientTileMode.MIRROR,
            rotation=math.pi / 3,
        ),
    )


def create_exp_lvl_display(lvl, exp):
    return ft.Container(
        ft.Column(
            [
                ft.Text(
                    f"LVL {lvl}",
                    size=14,
                    color=Colors.BLACK,
                    font_family="ConcertOne",
                ),
                ft.Text(
                    f"EXP {exp}/100",
                    size=14,
                    color=Colors.BLACK,
                    font_family="ConcertOne",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        margin=ft.margin.Margin(10, 0, 0, 0),
        padding=ft.padding.Padding(3, 2, 3, 2),
        bgcolor=Colors.ACCENT,
        border_radius=ft.border_radius.all(8),
        width=85,
        height=45,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.colors.BLACK54,
            offset=ft.Offset(0, 0),
        ),
    )


def create_life_hearts(life_hearts: str | int):
    hearts = [
        ft.Icon(name=ft.icons.FAVORITE_OUTLINED, color=ft.colors.RED, size=28)
        for _ in range(int(life_hearts))
    ]

    hearts_bordered = [
        ft.Icon(name=ft.icons.FAVORITE_BORDER, color=ft.colors.RED_900, size=28)
        for _ in range(3)
    ]

    return ft.Container(
        ft.Stack(
            controls=[
                ft.Row(controls=hearts_bordered, spacing=5),
                ft.Row(controls=hearts, spacing=5),
            ],
            width=(28 + 5) * 3,
            height=28,
            # bgcolor=Colors.WHITE, # for debug container size
        ),
        margin=ft.margin.Margin(10, 10, 10, 0),
    )


def create_currency_display(capycoins):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(
                    src=DBFields.CAPYCOIN,
                    width=24,
                    height=24,
                ),
                ft.Text(
                    str(capycoins),
                    color=ft.colors.BLACK,
                    size=14,
                    font_family="ConcertOne",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.Margin(10, 0, 10, 0),
        padding=ft.padding.all(5),
        # bgcolor=Colors.WHITE, # for debug container size
    )


def create_life_currency_display(life_hearts, capycoins):
    return ft.Column(
        [create_life_hearts(life_hearts), create_currency_display(capycoins)]
    )


def init_stats() -> None:
    stats_var = Session.get_logged_user().stats

    (DefaultComponents.STATISTICS_BAR.value.content[0].leading.content.controls).clear()

    hat_equipped = None
    color_equipped = None
    shirt_equipped = None

    for item in stats_var["inventory"]["hats"]:
        if item["isEquipped"]:
            hats_product = read_product_from_db("hats")
            hat_images = hats_product.images
            hat_equipped = hat_images[str(item["id"])]["url"]
            break

    for item in stats_var["inventory"]["colors"]:
        if item["isEquipped"]:
            colors_product = read_product_from_db("colors")
            color_images = colors_product.images
            color_equipped = color_images[str(item["id"])]["url"]
            break

    for item in stats_var["inventory"]["shirts"]:
        if item["isEquipped"]:
            shirts_product = read_product_from_db("shirts")
            shirt_images = shirts_product.images
            shirt_equipped = shirt_images[str(item["id"])]["url"]
            break

    DefaultComponents.STATISTICS_BAR.value.content[0].leading.content.controls.append(
        create_equipped_images(
            hat_equipped,
            color_equipped,
            shirt_equipped,
        )
    )

    DefaultComponents.STATISTICS_BAR.value.content[0].leading.content.controls.append(
        create_exp_lvl_display(stats_var["level"], stats_var["exp"])
    )

    DefaultComponents.STATISTICS_BAR.value.content[0].actions[0] = (
        create_life_currency_display(stats_var["life_hearts"], stats_var["capycoins"])
    )
    Page.update()
