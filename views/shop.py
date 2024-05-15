from views.view import View
from components.component import Component
from components.default_components import defaults
import flet as ft


# Dummy data
products = {
    "hats": {
        "name": "Hats",
        "images": [
            "https://lh3.googleusercontent.com/pw/AP1GczOjY162O6weUBUQCO2nG5cEUNjkiy2D6O0MTAZuWFeKzhjk4j40jiUg8R58n-E58pHG5aJCMbeS9nxIe1B4hDxXm-XrPGjnaTceh_69H_GrvaHiT2IVHzTedJiqN43r71xAwRC5CmAzUJz5y0vd_Kw=w642-h857-s-no-gm?authuser=0",
            "https://lh3.googleusercontent.com/pw/AP1GczOUOYrQC_n9_x1wK5JZcXxKf056b26QwigQ5ibqumcfzHyK-0zOEf9DiudOwSmWk5jJsRkLzTO28dhhuMTBZS3nxy_gfBNfFyPEVGyfPZcMq_OXU1gnQ0AhXjGF1yXQE1v4BmFKlwocUE0fHpy1guU=w642-h857-s-no-gm?authuser=0",
            "https://lh3.googleusercontent.com/pw/AP1GczM4rE9w5STaV4BiVE3TQ2MtuVCwYj1EB5YFs11fujKmZBkKy0u201GzbFOOvi-9wXJ11pDIJwnCakf5j5EVsbycVVdWHYLZsdKVusrvnPqfLjyVGOHtLwbKKs21Cavtr9nBYhrrkXzCa6Zxkcwn8NU=w642-h857-s-no-gm?authuser=0",
        ],
        "price": "100 PLN",
    },
    "colors": {
        "name": "Colors",
        "images": [
            "https://htmlcolorcodes.com/assets/images/colors/red-color-solid-background-1920x1080.png",
            "https://htmlcolorcodes.com/assets/images/colors/green-color-solid-background-1920x1080.png",
            "ft.Text(name, text_align=ft.TextAlign.CENTER),",
        ],
        "price": "50 PLN",
    },
    "shirts": {
        "name": "Shirts",
        "images": [
            "https://i.imgur.com/lEy6WEe.jpeg",
            "https://i.imgur.com/GyIhaOr.jpeg",
            "https://i.imgur.com/rXHNe2T.jpeg",
        ],
        "price": "150 PLN",
    },
}

hats_current_index = 0
colors_current_index = 0
shirts_current_index = 0


def get_product_data(product_id):
    return products.get(product_id)


def update_display(container, images, current_index):
    container.content.src = images[current_index]
    container.update()


def move_left(e, images, current_index_ref, container):
    if current_index_ref.current > 0:
        current_index_ref.current -= 1
        update_display(container, images, current_index_ref.current)


def move_right(e, images, current_index_ref, container):
    if current_index_ref.current < len(images) - 1:
        current_index_ref.current += 1
        update_display(container, images, current_index_ref.current)


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
    product_data = get_product_data(product_id)
    if not product_data:
        return None

    name = product_data["name"]
    price = product_data["price"]
    images = product_data["images"]

    container = ft.Container(
        content=ft.Image(
            src=images[index_ref.current], fit=ft.ImageFit.COVER, width=100, height=100
        ),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        width=200,
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
        controls=[
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
                        on_click=lambda e: move_left(e, images, index_ref, container),
                    ),
                    container,
                    ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD,
                        icon_color="blue400",
                        icon_size=20,
                        on_click=lambda e: move_right(e, images, index_ref, container),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Container(
                content=ft.ElevatedButton("Buy", on_click=open_dlg),
                alignment=ft.alignment.center,
            ),
            ft.Divider(),
        ]
    )


shop = View(name="Shop", route="/shop")


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

shop.add_component(defaults["STATISTICS_BAR"])
shop.add_component(defaults["NAVIGATION_BAR"])
print(shop)
