from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents, update_statistics_bar
from utils.enums import FletNames, Colors, DBFields
import flet as ft
from product import read_product_from_db
from session import Session
from page import Page


image_width = 250
image_height = 295.3
buttons_size = 20


def update_image(container, images, current_index):
    container.content.src = images[str(current_index)]["url"]
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

shop = View(name=FletNames.SHOP, route=f"/{FletNames.SHOP}")

# Basic buying/equiping functions
shop.var = {"inventory": {}}


def is_item_bought(group_name, item_id, inventory):
    for item in inventory.get(group_name, []):
        if item["id"] == item_id:
            return True
    return False


def equip_item(item_group, item_id):
    for item in shop.var["inventory"].get(item_group, []):
        if item["id"] == item_id:
            item["isEquipped"] = True
        else:
            item["isEquipped"] = False
    update_dto_inventory()


def insert_dto_data_to_inventory(item_group, item_ref_index):
    shop.var["inventory"][item_group].append(
        {"id": item_ref_index.current, "isEquipped": "False"}
    )
    update_dto_inventory()


def insert_dto_data_to_stats_currency(item_group):
    item = read_product_from_db(item_group)
    price = item.price
    stats_var = Session.get_logged_user().stats
    stats_var["capycoins"] = str(int(stats_var["capycoins"]) - int(price))


def update_dto_inventory():
    dto = Session.get_logged_user()
    dto.stats["inventory"] = shop.var["inventory"]
    services.save_file_data("stats", dto)


# Buy/Equip button functions for each item group
async def dismiss_dialog_hats(e):
    if is_item_bought("hats", hats_index_ref.current, shop.var["inventory"]):
        equip_item("hats", hats_index_ref.current)
    else:
        if e.control.text == "Buy":
            insert_dto_data_to_inventory("hats", hats_index_ref)
            insert_dto_data_to_stats_currency("hats")
    cupertino_alert_dialog.open = False
    await e.control.page.update_async()

    update_statistics_bar(e.control.page)


async def dismiss_dialog_colors(e):
    if is_item_bought("colors", colors_index_ref.current, shop.var["inventory"]):
        equip_item("colors", colors_index_ref.current)
    else:
        if e.control.text == "Buy":
            insert_dto_data_to_inventory("colors", colors_index_ref)
            insert_dto_data_to_stats_currency("colors")
    cupertino_alert_dialog.open = False
    await e.control.page.update_async()

    update_statistics_bar(e.control.page)


async def dismiss_dialog_shirts(e):
    if is_item_bought("shirts", shirts_index_ref.current, shop.var["inventory"]):
        equip_item("shirts", shirts_index_ref.current)
    else:
        if e.control.text == "Buy":
            insert_dto_data_to_inventory("shirts", shirts_index_ref)
            insert_dto_data_to_stats_currency("shirts")
    cupertino_alert_dialog.open = False
    await e.control.page.update_async()

    update_statistics_bar(e.control.page)


cupertino_alert_dialog = ft.CupertinoAlertDialog()


def open_dlg_hats(e):
    dto = Session.get_logged_user()
    if is_item_bought("hats", hats_index_ref.current, shop.var["inventory"]):
        button_text = "Equip"
    else:
        button_text = "Buy"
    e.control.page.dialog = cupertino_alert_dialog
    cupertino_alert_dialog.actions = [
        ft.CupertinoDialogAction(
            button_text, is_destructive_action=True, on_click=dismiss_dialog_hats
        ),
        ft.CupertinoDialogAction(text="Cancel", on_click=dismiss_dialog_hats),
    ]
    cupertino_alert_dialog.open = True
    e.control.page.update()


def open_dlg_colors(e):
    dto = Session.get_logged_user()
    if is_item_bought("colors", colors_index_ref.current, shop.var["inventory"]):
        button_text = "Equip"
    else:
        button_text = "Buy"
    e.control.page.dialog = cupertino_alert_dialog
    cupertino_alert_dialog.actions = [
        ft.CupertinoDialogAction(
            button_text, is_destructive_action=True, on_click=dismiss_dialog_colors
        ),
        ft.CupertinoDialogAction(text="Cancel", on_click=dismiss_dialog_colors),
    ]
    cupertino_alert_dialog.open = True
    e.control.page.update()


def open_dlg_shirts(e):
    dto = Session.get_logged_user()
    if is_item_bought("shirts", shirts_index_ref.current, shop.var["inventory"]):
        button_text = "Equip"
    else:
        button_text = "Buy"
    e.control.page.dialog = cupertino_alert_dialog
    cupertino_alert_dialog.actions = [
        ft.CupertinoDialogAction(
            button_text, is_destructive_action=True, on_click=dismiss_dialog_shirts
        ),
        ft.CupertinoDialogAction(text="Cancel", on_click=dismiss_dialog_shirts),
    ]
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
            src=hat_images[str(hats_index_ref.current)]["url"],
            fit=ft.ImageFit.CONTAIN,
            width=image_width,
            height=image_height,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TRANSPARENT,
    )

    color_container = ft.Container(
        content=ft.Image(
            src=color_images[str(colors_index_ref.current)]["url"],
            fit=ft.ImageFit.CONTAIN,
            width=image_width,
            height=image_height,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.TRANSPARENT,
    )

    shirt_container = ft.Container(
        content=ft.Image(
            src=shirt_images[str(shirts_index_ref.current)]["url"],
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
                                                        src=DBFields.CAPYCOIN,
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
                                    on_click=open_dlg_hats,
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
                                                        src=DBFields.CAPYCOIN,
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
                                    on_click=open_dlg_shirts,
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
                                                        src=DBFields.CAPYCOIN,
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
                                    on_click=open_dlg_colors,
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


def init_shop() -> None:
    dto = Session.get_logged_user()
    view_data = services.get_view_data(view_name=shop.name, user_id=dto.id)
    stats_var = dto.stats
    shop.var["inventory"] = stats_var.get("inventory", {})


shop.add_component(DefaultComponents.STATISTICS_BAR.value)
shop.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_shop_copy(shop)
shop.log()
