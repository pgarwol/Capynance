from views.view import View
from entities.spending_type import SpendingType
from utils.helpers import shuffle_dict, sort_dict_by_values_desc
from entities.income_source import IncomeSource
from itertools import islice
import utils.services as services
import pandas as pd
from session import Session
from enum import StrEnum
from utils.enums import (
    FletNames,
    Colors,
    String,
    DateFormat,
    Currencies,
    get_logo_src,
    get_theme_color,
)
from utils.styles import Style
from components.component import Component, DefaultComponents
from typing import Literal, Optional, Sequence
from page import Page
import random
import numpy as np
import flet as ft


finances = View(name=FletNames.FINANCES, route=f"/{FletNames.FINANCES}")
finances.add_component(DefaultComponents.STATISTICS_BAR.value)

finances.add_component(
    Component(
        content=[
            income_sources := ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                spacing=100,
            )
        ],
        description="User's spendings",
    )
)

finances.add_component(DefaultComponents.NAVIGATION_BAR.value)
finances.var = {"sources": []}


def generate_income_source_tile(
    name: str,
    logo_src: str,
    theme_color: Colors,
    money_in: float,
    money_out: float,
    saldo: float,
    period: str,
) -> ft.Row:
    """
    Generate an income source tile with specified details and styling.

    Args:
        name (str): The name of the income source.
        logo_src (str): The source URL for the logo of the income source.
        theme_color (Colors): The theme color for the tile.
        money_in (float): The amount of money coming in.
        money_out (float): The amount of money going out.
        saldo (float): The balance amount.
        period (str): The period for the income source.

    Returns:
        ft.Row: A Row object representing the generated income source tile.
    """
    _HEADER_SIZE = 32
    return ft.Row(
        controls=[
            ft.Image(width=120, height=120, src=logo_src),
            ft.Column(
                [
                    ft.Text(
                        f"{name.capitalize()}",
                        weight=ft.FontWeight.BOLD,
                        size=_HEADER_SIZE,
                        text_align=ft.TextAlign.CENTER,
                        **Style.Text.value,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"{money_out:.2f} {Currencies.POLISH_ZLOTY}",
                                weight=ft.FontWeight.BOLD,
                                size=_HEADER_SIZE // 2,
                                color=Colors.NEGATIVE,
                                **Style.Text.value,
                            ),
                            ft.Icon(
                                ft.icons.COMPARE_ARROWS_OUTLINED,
                                color=Colors.WHITE,
                                size=30,
                            ),
                            ft.Text(
                                f"{money_in:.2f} {Currencies.POLISH_ZLOTY}",
                                weight=ft.FontWeight.BOLD,
                                size=_HEADER_SIZE // 2,
                                color=Colors.POSITIVE,
                                **Style.Text.value,
                            ),
                        ]
                    ),
                    ft.Text(
                        f"Saldo: {saldo:.2f} {Currencies.POLISH_ZLOTY}",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        **Style.Text.value,
                    ),
                ],
                width=220,
                height=120,
            ),
        ],
    )


def append_item_to_finances(row: ft.Row) -> None:
    income_sources.controls.append(row)


def get_finance_data(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data).transpose().reset_index()
    df.columns = ["date", "in", "out"]
    df["date"] = pd.to_datetime(df["date"], format=str(DateFormat.dmY))
    df["in"] = df["in"].astype(float)
    df["out"] = df["out"].astype(float)
    df.set_index("date", inplace=True)
    df["net"] = df["in"].astype(int) - df["out"].astype(int)
    df["day"] = df.index.day

    return df


def retrieve_dto_data(dto) -> None:
    view_data = services.get_view_data(view_name=finances.name, user_id=dto.id)
    for source in view_data["sources"]:
        finances.var["sources"].append(
            IncomeSource(
                name=source,
                logo_src=get_logo_src(source),
                data=get_finance_data(view_data["sources"][source]),
                theme_color=get_theme_color(source),
            )
        )


def draw_money_flow_chart(
    data: pd.DataFrame, line_color: Optional[str] = Colors.PRIMARY_DARKER
) -> ft.LineChart:
    """
    Draws a line chart based on the provided data with customizable line color.

    Args:
        data (pd.DataFrame): The data to be visualized in the line chart.
        line_color (Optional[str], optional): The color of the line in the chart. Defaults to Colors.PRIMARY_DARKER.

    Returns:
        ft.LineChart: A LineChart object representing the drawn line chart.
    """

    def format_y_label(value: float) -> str:
        if value == 0:
            return "0"
        elif value >= 100.00:
            return f"{value / 1000}K"
        else:
            f"{value:.2f}"

    money_flow_data = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(x, float(y))
                for x, y in zip(data["day"].values, data["net"].values)
            ],
            stroke_width=5,
            color=line_color,
            curved=True,
            stroke_cap_round=True,
        )
    ]
    x_labels = [
        ft.ChartAxisLabel(
            value=day,
            label=ft.Container(
                ft.Text(
                    f"{day}", size=12, weight=ft.FontWeight.BOLD, **Style.Text.value
                ),
                expand=True,
            ),
        )
        for day in [1] + list(range(5, 31, 5))
    ]

    y_labels = [
        ft.ChartAxisLabel(
            value=y_val,
            label=ft.Container(
                ft.Text(
                    format_y_label(y_val),
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    **Style.Text.value,
                ),
                width=300,
                height=20,
                expand=True,
            ),
        )
        for y_val in [0, 500, 1000]
    ]

    min_x = data["day"].values.min()
    max_x = data["day"].values.max()
    min_y = 0.0 if data["net"].values.min() > 0.0 else data["net"].values.min() - 100
    max_y = data["net"].values.max()
    chart = ft.LineChart(
        data_series=money_flow_data,
        left_axis=ft.ChartAxis(labels=y_labels, labels_size=24, show_labels=True),
        bottom_axis=ft.ChartAxis(labels=x_labels, labels_size=24, show_labels=True),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, Colors.BLACK),
        min_x=min_x,
        max_x=max_x,
        min_y=min_y,
        max_y=max_y,
        vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.colors.GREY_900),
        expand=False,
    )
    return chart


def calculate_total_outcome(dataframes: Sequence[pd.DataFrame]) -> float:
    """
    Calculate the total sum of outcomes from a sequence of Pandas DataFrames.

    Args:
        dataframes (Sequence[pd.DataFrame]): A sequence of Pandas DataFrames containing outcome data.

    Returns:
        float: The total sum of outcomes calculated from the input DataFrames.
    """

    money_pool = 0.0
    for df in dataframes:
        money_pool += df["out"].sum()
    return money_pool


def randomize_outcome(
    money_pool: float, upper_threshold: Optional[float] = 0.2
) -> float:
    """
    Generate a random outcome within a specified range based on a money pool.

    Args:
        money_pool (float): The total amount of money available for the outcome.
        upper_threshold (Optional[float], optional): The upper limit threshold for the outcome. Defaults to 0.2.

    Returns:
        float: The randomized outcome rounded to 2 decimal places.
    """
    outcome = random.uniform(0.0, upper_threshold * money_pool)
    return np.round(outcome, 2)


def analyze_user_spendings(spending_types: Sequence[str], money_pool: float) -> dict:
    """Obviously this is fake method, all it does it distributes money to different categories"""

    categorized_outcome = {}
    for s_type in spending_types:
        randomized_outcome = randomize_outcome(money_pool)
        categorized_outcome[s_type] = randomized_outcome
        money_pool -= randomized_outcome

    return categorized_outcome


def reset_finances() -> None:
    """
    Reset the finances by clearing the income sources controls and financial sources variables.
    """
    income_sources.controls.clear()
    finances.var["sources"].clear()


def init_finances() -> None:
    reset_finances()
    retrieve_dto_data(dto=Session.get_logged_user())
    for source in finances.var["sources"]:
        append_item_to_finances(
            generate_income_source_tile(
                name=source.name,
                logo_src=source.logo_src,
                theme_color=source.theme_color,
                money_in=source.data["in"].sum(),
                money_out=source.data["out"].sum(),
                saldo=source.data["net"].sum(),
                period=f"{source.data.index.month[0]}.{source.data.index.year[0]}",
            )
        )

        append_item_to_finances(
            ft.Container(
                draw_money_flow_chart(source.data, source.theme_color),
                height=200,
                width=460,
                padding=8,
            )
        )

    append_item_to_finances(
        top_spendings_categories := ft.DataTable(
            sort_ascending=True,
            columns=[ft.DataColumn(ft.Text(String.EMPTY)) for _ in range(3)],
            rows=[],
        )
    )

    spending_types = SpendingType.get_instances()
    processed_spendings = analyze_user_spendings(
        spending_types=list(shuffle_dict(spending_types).keys()),
        money_pool=calculate_total_outcome(
            [
                finances.var["sources"][i].data
                for i, _ in enumerate(finances.var["sources"])
            ]
        ),
    )

    spendings_rows_to_generate = 5
    for spending_type in islice(
        sort_dict_by_values_desc(processed_spendings), spendings_rows_to_generate
    ):
        top_spendings_categories.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(spending_types[spending_type]["icon"]),
                    ft.DataCell(
                        ft.Text(
                            spending_types[spending_type]["full_name"],
                            **Style.Text.value,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            f"{processed_spendings[spending_type]:.2f} {Currencies.POLISH_ZLOTY}",
                            **Style.Text.value,
                        )
                    ),
                ],
            )
        )

    Page.update()


finances.log()
