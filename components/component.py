from utils.enums import Colors, FletNames
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


class Stats:
    def __init__(
        self,
        hats_owned: str,
        hat_equiped: str,
        capy_colors_owned: str,
        capy_color_equiped: str,
        shirts_owned: str,
        shirt_equiped: str,
        life_hearts: int,
        capycoins: int,
        level: str,
        exp: str,
    ):
        self.hats_owned = hats_owned
        self.hat_equiped = hat_equiped
        self.capy_colors_owned = capy_colors_owned
        self.capy_color_equiped = capy_color_equiped
        self.shirts_owned = shirts_owned
        self.shirt_equiped = shirt_equiped
        self.life_hearts = life_hearts
        self.capycoins = capycoins
        self.level = level
        self.exp = exp


stats = FletNames.STATS
stats.var = {}


# life_hearts = 3
default_equipped = "https://lh3.googleusercontent.com/pw/AP1GczP22h9zKEFj7hcIiX-9gfwtRm-W8KPJSP-oYdHEt-0pvgZPy0QOduH8KnGHpC9UFQHT2O_m3jTDisvzGqPEDiWxlC6AFGXdoeFzUYenecjZtIn38Xy-7MbRwAD7tN-iH_OM2iw13cy_YdzpixrzK0E=w725-h857-s-no-gm?authuser=0"
color_equipped = "https://lh3.googleusercontent.com/pw/AP1GczMPMqur_kGbQI-lEY3s8MWERxHPlyNACTOdhCL_hIZYA-rv_FDTz66K6p0szt1OB9r713_Zx8XX41QeM_z-NpZFdB46B6CxLlN_BDZKjBu0y85gVCYHHQc01K5KiD9En7ev3w919g6yI8z2ETzyjD0=w725-h857-s-no-gm?authuser=0"
shirt_equipped = "https://lh3.googleusercontent.com/pw/AP1GczON_1lHKkFaB3SN3_qU8nYcZA5c5K4naoRar75J6q1ItXLQV6v2KsIy1d4scUioAAnG7MNpuIlysF4bZ72s-imm0ulEtdjBNiwo_AL8QC1jXyVz1dL0Eoj_2T8DxS2PVesX5t0CStXdsPNDmW_FBgs=w725-h857-s-no-gm?authuser=0"
hat_equipped = "https://lh3.googleusercontent.com/pw/AP1GczOwMmGFN8ARlJ8PqmmdaOP2tgfzPATP2l28Ih1r0myvynQLRr_pvSVMkpdQWE2nntU8GVxVK37CzdG2s1m68NDkQdaO-j-lrlNHoapJU0JzBZCviE_lXzUJyBJQtPJpV3iuMhAJvYeV8O4A0K46blM=w725-h857-s-no-gm?authuser=0"

capycoins = 20000
lvl = 10
exp = 110
exp_img = "https://static.wikia.nocookie.net/minecraft/images/0/0a/ExperienceOrb.gif/revision/latest/smart/width/371/height/332?cb=20190907041203"

life_hearts = None
# hat_equiped = stats.var["hat_equiped"]
# capycoins = stats.var["capycoins"]


def create_life_hearts(life_hearts):
    print(stats.var["life_hearts"])
    if stats.var is None or "life_hearts" not in stats.var:
        return ft.Text("blad")
    hearts = [
        ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.RED, size=28)
        for _ in range(int(stats.var["life_hearts"]))
        # for _ in range(life_hearts)
    ]
    return ft.Row(controls=hearts, spacing=5)


image_width = 75
image_height = (71 * image_width) / 60


def create_equipped_images(hat_img, color_img, shirt_img, default_img):
    controls = []

    if color_img:
        controls.append(
            ft.Image(
                src=color_equipped,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    if hat_img:
        controls.append(
            ft.Image(
                src=hat_equipped,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    if shirt_img:
        controls.append(
            ft.Image(
                src=shirt_equipped,
                fit=ft.ImageFit.CONTAIN,
                width=image_width,
                height=image_height,
            )
        )

    if not controls:
        controls.append(
            ft.Image(
                src=default_equipped,
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
        # clip_behavior=ft.ClipBehavior.HARD_EDGE,
        width=85,
        height=85,
        border=ft.border.all(2, Colors.ACCENT),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.colors.GREY,
            offset=ft.Offset(0, 0),
        ),
    )


def create_currency_display(capycoins):
    return ft.Row(
        controls=[
            ft.Image(
                src="https://lh3.googleusercontent.com/pw/AP1GczNFNx7f733rhrtzgyaB22YjoMxkNio2F4u9eMEW4milxdp3RU82RsAF2p0S5DR-rVfZYhqXtukjwKk0dF7O_MIEsFm0-Wfvdts8FRRj_VTq7oizSUZLhsKmDBv7SLm3yo45gT9rWtRBCMKrPz5z_CI=w857-h857-s-no-gm?authuser=0",
                width=36,
                height=36,
            ),
            ft.Text(capycoins, color=ft.colors.BLACK),
        ]
    )


class DefaultComponents(Enum):
    DEFAULT_MENU_SELECTION = 3

    STATISTICS_BAR = Component(
        content=[
            ft.AppBar(
                leading=ft.Row(
                    # controls=[
                    #     create_life_hearts(
                    #         stats.var["life_hearts"]
                    #         if stats.var is not None
                    #         else ""
                    #         # life_hearts
                    #     ),
                    # ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                title=ft.Container(
                    content=create_equipped_images(
                        hat_equipped, color_equipped, shirt_equipped, default_equipped
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.Padding(0, 0, 0, 0),  # Ensure no extra padding
                    margin=ft.Margin(0, 0, 0, 0),  # Ensure no extra margin
                    width=image_width,
                    height=image_height,
                ),
                actions=[
                    create_currency_display(capycoins),
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
                    selected_index=3,
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
                                name=ft.icons.CALENDAR_MONTH,
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
                                name=ft.icons.ATTACH_MONEY,
                                color=Colors.BLACK,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(name=ft.icons.PEOPLE, color=Colors.BLACK),
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 10),
                            content=ft.Icon(
                                name=ft.icons.SETTINGS_ROUNDED,
                                color=Colors.BLACK,
                            ),
                        ),
                    ],
                    **Style.CupertinoSlidingSegmentedButton.value
                )
            )
        ],
        description="Contains bottom navigation bar.",
    )

    # stats.var.append(
    #     Stats(
    #         hats_owned=view_data["hats_owned"],
    #         hat_equiped=view_data["hat_equiped"],
    #         capy_colors_owned=view_data["capy_colors_owned"],
    #         capy_color_equiped=view_data["capy_color_equiped"],
    #         shirts_owned=view_data["shirts_owned"],
    #         shirt_equiped=view_data["shirt_equiped"],
    #         life_hearts=int(view_data["life_hearts"]),
    #         capycoins=int(view_data["capycoins"]),
    #         level=view_data["level"],
    #         exp=view_data["exp"],
    #     )
    # )


def init_stats() -> None:
    if "life_hearts" in stats.var and stats.var is not None:
        DefaultComponents.STATISTICS_BAR.value.content[0].leading[0].controls = (
            create_life_hearts(stats.var["life_hearts"])
        )
