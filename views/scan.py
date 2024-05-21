from views.view import View, ViewsInitialStates
import utils.services as services
from components.component import Component, DefaultComponents
from pathlib import Path
from utils.enums import FletNames, String, DBFields
from utils.styles import Style
import pandas as pd
import flet as ft
from typing import List, Tuple
import random


scan = View(name=FletNames.SCAN, route=f"/{FletNames.SCAN}")
scan.add_component(DefaultComponents.STATISTICS_BAR.value)
scan.add_component(
    Component(
        [ft.Text("SKANOWANIE PARAGONU", **Style.Text.value)],
        description="View representing scanning QR codes.",
    )
)
scan.add_component(
    Component(
        content=[receipt_col := ft.Column()],
        description="Receipt.",
    )
)

products = pd.read_csv(Path(DBFields.RELATIVE_DB_PATH + "products.csv").resolve())


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
        rows.append(ft.Text(f"{product:_<25} {price:.2f} ZŁ", **Style.Text.value))

    rows.extend(
        (
            ft.Text(f"{String.EMPTY:_<25}", **Style.Text.value),
            ft.Text(f"{String.EMPTY:_<25} {total_price:.2f} ZŁ", **Style.Text.value),
        )
    )
    return rows


def init_scan() -> None:
    receipt_col.controls = generate_n_receipt_rows(n=5)


scan.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_scan_copy(scan)
scan.log()
