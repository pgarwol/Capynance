from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents
from utils.products import (
    get_cheaper_alternatives_dict,
    products,
    has_cheaper_alternatives,
    count_cheaper_alternatives,
)
from pathlib import Path
import flet_core
from utils.enums import FletNames, String, DBFields, Colors, Currencies
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
                    ft.Container(bgcolor=Colors.BLACK, width=320, height=350),
                    ft.IconButton(
                        icon=ft.icons.CAMERA_ALT_ROUNDED,
                        icon_color=Colors.WHITE,
                        icon_size=40,
                        tooltip="Scan receipt",
                        on_click=lambda _: scan_receipt(),
                        bgcolor=Colors.ACCENT,
                    ),
                    receipt := ft.DataTable(
                        sort_ascending=True,
                        columns=[
                            ft.DataColumn(ft.Text(String.EMPTY)) for _ in range(3)
                        ],
                        rows=[],
                    ),
                ],
            )
        ],
        description="Button and 'camera'",
    )
)


def scroll_to_receipt():
    page_column.scroll_to(key="0", duration=1000)


def get_random_product(products: pd.DataFrame) -> Tuple[str, float]:
    random_row = products.sample(n=1).iloc[0]
    product_name = random_row["Product"]
    product_price = random_row["Price (PLN)"]
    return product_name, product_price


def clear_receipt() -> None:
    receipt.rows.clear()


def on_confirm(e: flet_core.control_event.ControlEvent) -> None:
    e.page.dialog.open = False
    e.page.update()


def generate_alternatives_rows_from_dict(alternatives: dict) -> list[ft.DataRow]:
    print(alternatives.items())
    return [
        ft.DataRow(
            [
                ft.DataCell(ft.Text(alternative["Product"], **Style.Text.value)),
                ft.DataCell(
                    ft.Text(f'{alternative["Price (PLN)"]:.2f} ZŁ', **Style.Text.value)
                ),
            ]
        )
        for _, alternative in alternatives.items()
    ]


def get_alternatives_as_popup(product_name: str):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(
            f"Znaleziono {count_cheaper_alternatives(product_name, products)} tańszych alternatyw \n dla {product_name}!",
            color=Colors.ACCENT,
            weight=ft.FontWeight.BOLD,
            **Style.Text.value,
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    alternatives_datatable := ft.DataTable(
                        sort_ascending=True,
                        columns=[
                            ft.DataColumn(ft.Text("Produkt", **Style.Text.value)),
                            ft.DataColumn(ft.Text("Oszczędzisz", **Style.Text.value)),
                        ],
                        rows=list(
                            generate_alternatives_rows_from_dict(
                                get_cheaper_alternatives_dict(product_name, products)
                            )
                        ),
                    )
                ],
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            height=300,
        ),
        actions=[
            ft.TextButton(
                text="Ok!",
                on_click=on_confirm,
                style=ft.ButtonStyle(color=Colors.ACCENT),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


def display_alternatives(
    product_name: str, e: flet_core.control_event.ControlEvent
) -> None:
    alternatives_popup = get_alternatives_as_popup(product_name)
    try:
        e.page.dialog = alternatives_popup
        alternatives_popup.open = True
        e.page.update()
    except Exception as e:
        print(f"An error occurred: {e}")


def display_alternatives_wrapper(product_name: str):
    def wrapper(e: flet_core.control_event.ControlEvent):
        display_alternatives(product_name, e)

    return wrapper


def generate_n_receipt_rows(n: int) -> None:
    clear_receipt()
    total_price = 0.0

    for _ in range(n):
        product, price = get_random_product(products)
        total_price += price

        has_alternatives = has_cheaper_alternatives(product, products)

        receipt.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.PRIORITY_HIGH_OUTLINED,
                            on_click=display_alternatives_wrapper(product),
                            icon_color=Colors.ACCENT,
                        )
                        if has_alternatives
                        else ft.Text(String.EMPTY)
                    ),
                    ft.DataCell(ft.Text(product, **Style.Text.value)),
                    ft.DataCell(
                        ft.Text(
                            f"{price:.2f} {Currencies.POLISH_ZLOTY}",
                            **Style.Text.value,
                            key=str(_),
                        )
                    ),
                ]
            )
        )

    receipt.rows.append(
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(String.EMPTY)),
                ft.DataCell(
                    ft.Text("Total: ", color=Colors.ACCENT, **Style.Text.value)
                ),
                ft.DataCell(
                    ft.Text(
                        f"{total_price:.2f} {Currencies.POLISH_ZLOTY}",
                        color=Colors.ACCENT,
                        weight=ft.FontWeight.BOLD,
                        **Style.Text.value,
                    )
                ),
            ]
        )
    )


def scan_receipt() -> None:
    """
    Generates the receipt. It is mockup of real world receipt scanning.

    Args:
        None

    Returns:
        None
    """

    generate_n_receipt_rows(n=random.randint(1, 15))
    Page.update()
    scroll_to_receipt()


def init_scan() -> None: ...


scan.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_scan_copy(scan)
scan.log()
