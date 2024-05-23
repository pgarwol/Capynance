from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents
from pathlib import Path
from utils.enums import FletNames, String, DBFields, Colors
from utils.styles import Style
import pandas as pd
from page import Page
import flet as ft
from typing import List, Tuple, Optional
import random


scan = View(name=FletNames.SCAN, route=f"/{FletNames.SCAN}")
scan.add_component(DefaultComponents.STATISTICS_BAR.value)
scan.add_component(
    Component(
        [
            page_column := ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                auto_scroll=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Lottie(
                        src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHZ0ZnIxaWx0a3poeXg3MTBjMnRudG5tMWQwNXk4MzBzOGgwMXB4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7bu3XilJ5BOiSGic/giphy.gif",
                        repeat=False,
                        reverse=False,
                        animate=True,
                    ),
                    ft.Container(bgcolor=Colors.BLACK, width=320, height=420),
                    ft.IconButton(
                        icon=ft.icons.CAMERA_ALT_ROUNDED,
                        icon_color=Colors.WHITE,
                        icon_size=40,
                        tooltip="Scan receipt",
                        on_click=lambda _: scan_receipt(),
                        bgcolor=Colors.ACCENT,
                    ),
                    receipt_col := ft.Column(),
                ],
            )
        ],
        description="Button and 'camera'",
    )
)


def scroll_to_receipt():
    page_column.scroll_to(key="0", duration=1000)


LINE_LENGTH = 45


def fill_str_with_spaces(
    product_name: str, symbol: Optional[str] = String.SPACE
) -> str:
    length = LINE_LENGTH
    spaces_to_fill = length - len(product_name)
    return f"{product_name}{spaces_to_fill*symbol}"


products = pd.read_csv(Path(DBFields.RELATIVE_DB_PATH + "products.csv").resolve())
products["Product"] = products["Product"].apply(fill_str_with_spaces)


def get_random_product(products: pd.DataFrame) -> Tuple[str, float]:
    random_row = products.sample(n=1).iloc[0]
    product_name = random_row["Product"]
    product_price = random_row["Price (PLN)"]
    return product_name, product_price


def generate_n_receipt_rows(n: int) -> List[ft.Row]:
    rows = []
    total_price = 0
    for _ in range(n):
        product, price = get_random_product(products)
        total_price += price
        rows.append(
            ft.Text(f"{product:}{price:.2f} ZŁ", **Style.Text.value, key=str(_))
        )

    rows.extend(
        (
            ft.Text(f"{(LINE_LENGTH+8)*'-'}", **Style.Text.value),
            ft.Text(
                f"{(LINE_LENGTH+8)*String.SPACE}{total_price:.2f} ZŁ",
                **Style.Text.value,
            ),
        )
    )
    return rows


def scan_receipt() -> None:
    receipt_col.controls = generate_n_receipt_rows(n=random.randint(1, 15))
    Page.update()
    scroll_to_receipt()


def init_scan() -> None: ...  # receipt_col.controls = generate_n_receipt_rows(n=5)


scan.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_scan_copy(scan)
scan.log()
