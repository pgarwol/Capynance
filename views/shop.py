from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents
from utils.enums import FletNames, Colors
import flet as ft
from product import read_product_from_db

image_width = 250
image_height = 295.3
buttons_size = 20
coin_img = "https://lh3.googleusercontent.com/pw/AP1GczNFNx7f733rhrtzgyaB22YjoMxkNio2F4u9eMEW4milxdp3RU82RsAF2p0S5DR-rVfZYhqXtukjwKk0dF7O_MIEsFm0-Wfvdts8FRRj_VTq7oizSUZLhsKmDBv7SLm3yo45gT9rWtRBCMKrPz5z_CI=w857-h857-s-no-gm?authuser=0"


def update_image(container, images, current_index):
    container.content.src = images[current_index]
    container.update()


def move_img_left(e, images, current_index_ref, container):
    if current_index_ref.current > 0:
        current_index_ref.current -= 1
        update_image(container, images, current_index_ref.current)


def move_img_right(e, images, current_index_ref, container):
    if current_index_ref.current < len(images) - 1:
        current_index_ref.current += 1

        update_image(container, images, current_index_ref.current)


hats_current_index = 0
colors_current_index = 0
shirts_current_index = 0

hats_index_ref = ft.Ref[int]()
hats_index_ref.current = hats_current_index

colors_index_ref = ft.Ref[int]()
colors_index_ref.current = colors_current_index

shirts_index_ref = ft.Ref[int]()
shirts_index_ref.current = shirts_current_index


# Buy button
async def dismiss_dialog(e):
    cupertino_alert_dialog.open = False
    await e.control.page.update_async()


cupertino_alert_dialog = ft.CupertinoAlertDialog(
    title=ft.Text("Do you want to buy this"),
    actions=[
        ft.CupertinoDialogAction(
            "Buy", is_destructive_action=True, on_click=dismiss_dialog
        ),
        ft.CupertinoDialogAction(text="Cancel", on_click=dismiss_dialog),
    ],
)


def open_dlg(e):
    e.control.page.dialog = cupertino_alert_dialog
    cupertino_alert_dialog.open = True
    e.control.page.update()


def create_shop_item(hats_id, colors_id, shirts_id):
    hats_product = read_product_from_db(hats_id)
    colors_product = read_product_from_db(colors_id)
    shirts_product = read_product_from_db(shirts_id)

    hat_images = hats_product.images
    color_images = colors_product.images
    shirt_images = shirts_product.images

    hat_container = ft.Container(
        content=ft.Image(
            src=hat_images[hats_index_ref.current],
            fit=ft.ImageFit.CONTAIN,
            width=image_width,
            height=image_height,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TRANSPARENT,
    )

    color_container = ft.Container(
        content=ft.Image(
            src=color_images[colors_index_ref.current],
            fit=ft.ImageFit.CONTAIN,
            width=image_width,
            height=image_height,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TRANSPARENT,
    )

    shirt_container = ft.Container(
        content=ft.Image(
            src=shirt_images[shirts_index_ref.current],
            fit=ft.ImageFit.CONTAIN,
            width=image_width,
            height=image_height,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TRANSPARENT,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    icon_color=Colors.PRIMARY_LIGHTER,
                                    icon_size=buttons_size,
                                    on_click=lambda e: move_img_left(
                                        e, hat_images, hats_index_ref, hat_container
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    icon_color=Colors.PRIMARY_LIGHTER,
                                    icon_size=buttons_size,
                                    on_click=lambda e: move_img_left(
                                        e,
                                        color_images,
                                        colors_index_ref,
                                        color_container,
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ARROW_BACK,
                                    icon_color=Colors.PRIMARY_LIGHTER,
                                    icon_size=buttons_size,
                                    on_click=lambda e: move_img_left(
                                        e,
                                        shirt_images,
                                        shirts_index_ref,
                                        shirt_container,
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ),
                        ft.Stack(
                            [
                                color_container,
                                shirt_container,
                                hat_container,
                            ],
                            width=image_width,
                            height=image_height,
                        ),
                        ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.ARROW_FORWARD,
                                    icon_color=Colors.PRIMARY_LIGHTER,
                                    icon_size=buttons_size,
                                    on_click=lambda e: move_img_right(
                                        e, hat_images, hats_index_ref, hat_container
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ARROW_FORWARD,
                                    icon_color=Colors.PRIMARY_LIGHTER,
                                    icon_size=buttons_size,
                                    on_click=lambda e: move_img_right(
                                        e,
                                        color_images,
                                        colors_index_ref,
                                        color_container,
                                    ),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ARROW_FORWARD,
                                    icon_color=Colors.PRIMARY_LIGHTER,
                                    icon_size=buttons_size,
                                    on_click=lambda e: move_img_right(
                                        e,
                                        shirt_images,
                                        shirts_index_ref,
                                        shirt_container,
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=200,
                    width=350,
                ),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Czapka",
                                                size=12,
                                                color=Colors.BLACK,
                                                font_family="ConcertOne",
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Image(
                                                        src=coin_img,
                                                        width=18,
                                                        height=18,
                                                    ),
                                                    ft.Text(
                                                        f" {hats_product.price}",
                                                        size=12,
                                                        color=Colors.BLACK,
                                                        font_family="ConcertOne",
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    on_click=open_dlg,
                                    color=Colors.BLACK.value,
                                    bgcolor=Colors.ACCENT.value,
                                    width=105,
                                    height=42,
                                ),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Ubranko",
                                                size=12,
                                                color=Colors.BLACK,
                                                font_family="ConcertOne",
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Image(
                                                        src=coin_img,
                                                        width=18,
                                                        height=18,
                                                    ),
                                                    ft.Text(
                                                        f" {shirts_product.price}",
                                                        size=12,
                                                        color=Colors.BLACK,
                                                        font_family="ConcertOne",
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    on_click=open_dlg,
                                    color=Colors.BLACK.value,
                                    bgcolor=Colors.ACCENT.value,
                                    width=105,
                                    height=42,
                                ),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Column(
                                        [
                                            ft.Text(
                                                "Kolor",
                                                size=12,
                                                color=Colors.BLACK,
                                                font_family="ConcertOne",
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Image(
                                                        src=coin_img,
                                                        width=18,
                                                        height=18,
                                                    ),
                                                    ft.Text(
                                                        f" {colors_product.price}",
                                                        size=12,
                                                        color=Colors.BLACK,
                                                        font_family="ConcertOne",
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    on_click=open_dlg,
                                    color=Colors.BLACK.value,
                                    bgcolor=Colors.ACCENT.value,
                                    width=105,
                                    height=42,
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    width=350,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )


shop = View(name=FletNames.SHOP, route=f"/{FletNames.SHOP}")

shop.add_component(
    Component(
        [
            ft.Row(
                [
                    create_shop_item("hats", "colors", "shirts"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        ],
        "Row with purchasable items",
    )
)
shop.var = {
    "selected_hat": None,
}
shop.add_component(DefaultComponents.STATISTICS_BAR.value)
shop.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_shop_copy(shop)
shop.log()
