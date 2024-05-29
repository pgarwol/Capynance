import pandas as pd
from utils.enums import Colors


class IncomeSource:
    def __init__(
        self, name: str, logo_src: str, data: pd.DataFrame, theme_color: Colors
    ):
        self.name = name
        self.logo_src = logo_src
        self.data = data
        self.theme_color = theme_color
