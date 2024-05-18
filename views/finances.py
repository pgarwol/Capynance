from views.view import View, ViewsInitialStates
import utils.services as services
import pandas as pd
from session import Session
from enum import StrEnum
from utils.enums import FletNames, Colors
from components.component import Component, DefaultComponents
from typing import Literal
from page import Page
import flet as ft


class SourcePhotos(StrEnum):
    APPLE_PAY = "https://lh3.googleusercontent.com/pw/AP1GczN-HOJWx3vEDSrBzchYoPQrJ-KS6P1owlvTurUMc1PV-XAxM_lSMdrsI4Zph_E6zaVUIrVSJOrrZHhfKrcvOxH86HEGeRAC3Oh2dyW1YIHxM0ooe93kEgEfmLsg3HK5C2FOGlu04Sk4zvAlIDLPMRk=w160-h160-s-no-gm"
    MBANK = "https://lh3.googleusercontent.com/pw/AP1GczMGmclVSSzuCUoWlVTmhjYvo42j1mI9LZ6hQDH3uwuD2na9Extl4EEnntFDn1a4DaWahK9trRvVKJqb2HFC9zq3lxQWiuumXufGH2NBO-7gwTpFXWwYqQofoYyBAdxKm1le5FOWXSInDhYa47dYjvY=w160-h160-s-no-gm"
    REVOLUT = "https://lh3.googleusercontent.com/pw/AP1GczO3xHEolUpxRVqhfpa3Aw2xFjG5s0ILBc3ui7kaWydz53nwpnipkJNjKMXFnSocEitxIVi5YhPUyxk5P2fawavPz-gX4HeVuO9Z9NwxfqBja8OhjkQktqCeO7YMRgFty76IDofVMriFXzyvptcIQQk=w160-h160-s-no-gm"
    SANTANDER = "https://lh3.googleusercontent.com/pw/AP1GczMgTKDgaFIH_9R5tCXLvM-8Jqg3tAbhymE0fL1K0s2AOhvceaLmdL7f-OuckyAr2y7eDUbhrmc5b1CWyO_ztxfOjwqYNY8K6VjXjpGb7CihezWKr8C3-WgJ33MHuFaP7YgOKwR_NFPQroev0WvKSSA=w160-h160-s-no-gm"
    PAYPAL = "https://lh3.googleusercontent.com/pw/AP1GczNOzTr0GdXO-W3k_TRwokN8MHnlPrf0VJkOEZAVhfqPOVCODIzHZ8irFHlrWstom5gqt2Ueu483ZR2lCgf0U_tm3u-4xXez8U5uE1wK77naoeFiE-owfCWR_SQ1OvZiEio5On6rx7t8FzhCXvE6rOc=w160-h160-s-no-gm"
    ING = "https://lh3.googleusercontent.com/pw/AP1GczOPgwLTS1Z4qBKqZ9MWSZZtDa6wV1XFZPp2mp1NwDTp4WYj4e0ejARbQfXLSTYresfgdhFGaIXLzvsz4ZjAwtK1UalZn4f_jByZKrFVZxfjujK5POfWqMG5llLlR5pjgPwZMDxnEGKRKrJEwJd8spc=w160-h160-s-no-gm"


finances = View(name=FletNames.FINANCES, route=f"/{FletNames.FINANCES}")
finances.add_component(DefaultComponents.STATISTICS_BAR.value)

finances.add_component(
    Component(
        content=[
            income_sources := ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            )
        ],
        description="User's spendings",
    )
)
finances.add_component(
    Component(
        content=[
            ft.Image(
                width=150,
                height=150,
                src="https://img.freepik.com/premium-wektory/happy-piggy-bank-maskotka-design_35422-31.jpg?w=1060",
            ),
            ft.Text("Udało ci się oszczędzić: xx.xx ZŁ!"),
        ],
        description="Money box",
    )
)

finances.add_component(DefaultComponents.NAVIGATION_BAR.value)
finances.var = {"sources": []}

finances.log()


def generate_income_source_tile(
    name: str,
    logo_src: str,
    theme_color: Colors,
    money_in: float,
    money_out: float,
    saldo: float,
    period: str,
) -> ft.Row:
    return ft.Row(
        controls=[
            ft.Image(width=120, height=120, src=logo_src),
            ft.Column(
                [
                    ft.Text(
                        f"{name.capitalize()} | {period}",
                        weight=ft.FontWeight.BOLD,
                        size=32,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                f"{money_out:.2f} ZŁ",
                                weight=ft.FontWeight.BOLD,
                                size=16,
                                color=Colors.NEGATIVE,
                            ),
                            ft.Icon(
                                ft.icons.COMPARE_ARROWS_OUTLINED,
                                color=Colors.WHITE,
                                size=30,
                            ),
                            ft.Text(
                                f"{money_in:.2f} ZŁ",
                                weight=ft.FontWeight.BOLD,
                                size=16,
                                color=Colors.POSITIVE,
                            ),
                        ]
                    ),
                    ft.Text(
                        f"Saldo: {saldo:.2f} ZŁ",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                width=300,
                height=120,
                alignment=theme_color,
            ),
        ],
    )


def append_income_source(row: ft.Row) -> None:
    income_sources.controls.append(row)


class IncomeSource:
    def __init__(
        self, name: str, logo_src: str, data: pd.DataFrame, theme_color: Colors
    ):
        self.name = name
        self.logo_src = logo_src
        self.data = data
        self.theme_color = data


def get_logo_src(source_name: str):
    match source_name.lower():
        case "mbank":
            return SourcePhotos.MBANK
        case "ing":
            return SourcePhotos.ING
        case "revolut":
            return SourcePhotos.REVOLUT
        case "paypal":
            return SourcePhotos.PAYPAL
        case "santander":
            return SourcePhotos.SANTANDER
        case "applePay":
            return SourcePhotos.APPLE_PAY
        case _:
            print("Invalid input")


def get_theme_color(source_name: str):
    match source_name.lower():
        case "mbank":
            return Colors.MBANK
        case "ing":
            return Colors.ING
        case "revolut":
            return Colors.REVOLUT
        case "paypal":
            return Colors.PAYPAL
        case "santander":
            return Colors.SANTANDER
        case "applePay":
            return Colors.APPLE_PAY
        case _:
            print("Invalid input")


def get_finance_data(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data).transpose().reset_index()
    df.columns = ["date", "in", "out"]
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["in"] = df["in"].astype(float)
    df["out"] = df["out"].astype(float)
    # Set 'date' column as the index
    df.set_index("date", inplace=True)
    df["net"] = df["in"].astype(int) - df["out"].astype(int)
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


def reset_finances() -> None:
    income_sources.controls.clear()
    finances.var["sources"].clear()


def init_finances() -> None:
    retrieve_dto_data(dto=Session.get_logged_user())
    for source in finances.var["sources"]:
        append_income_source(
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
    Page.update()
