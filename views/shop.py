from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents
from utils.enums import FletNames
import flet as ft
from product import read_product_from_db


hats_current_index = 0
colors_current_index = 0
shirts_current_index = 0


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
    # content=ft.Text("Do you want to buy this item?"),
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


def create_shop_item(product_id, index_ref):
    product = read_product_from_db(product_id)
    if not product:
        return None

    name = product.name
    price = product.price
    images = product.images

    container = ft.Container(
        content=ft.Image(
            src=images[index_ref.current], fit=ft.ImageFit.COVER, width=150, height=150
        ),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        width=150,
        height=150,
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=3,
            blur_radius=5,
            color=ft.colors.WHITE10,
            offset=ft.Offset(0, 0),
        ),
    )

    return ft.Column(
        controls=(
            ft.Container(
                content=ft.Text(name),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Text(price),
                alignment=ft.alignment.center,
            ),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="blue400",
                        icon_size=20,
                        on_click=lambda e: move_img_left(
                            e, images, index_ref, container
                        ),
                    ),
                    container,
                    ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD,
                        icon_color="blue400",
                        icon_size=20,
                        on_click=lambda e: move_img_right(
                            e, images, index_ref, container
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Container(
                content=ft.ElevatedButton("Buy", on_click=open_dlg),
                alignment=ft.alignment.center,
            ),
            ft.Divider(),
        )
    )


shop = View(name=FletNames.SHOP, route=f"/{FletNames.SHOP}")


shop.add_component(
    Component(
        [
            ft.Column(
                [
                    create_shop_item("hats", hats_index_ref),
                    create_shop_item("colors", colors_index_ref),
                    create_shop_item("shirts", shirts_index_ref),
                ],
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
            )
        ],
        "test",
    )
)

shop.add_component(DefaultComponents.STATISTICS_BAR.value)
shop.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_shop_copy(shop)
shop.log()
