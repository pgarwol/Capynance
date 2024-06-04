import pandas as pd
from utils.enums import DBFields
from pathlib import Path

products = pd.read_csv(Path(DBFields.RELATIVE_DB_PATH + "products_with_categories.csv").resolve())

subgroups_dict = {}
for category, group in products.groupby('Category'):
    sorted_group = group.sort_values(by='Price (PLN)')
    subgroups_dict[category] = sorted_group

def get_cheaper_alternatives(row: pd.Series, dataframe: pd.DataFrame):
    """
    Returns all cheaper alternatives for a given row in the DataFrame.

    Parameters:
    row (pd.Series): The row of the DataFrame to find cheaper alternatives for.
    dataframe (pd.DataFrame): The DataFrame to search within.

    Returns:
    pd.DataFrame: A DataFrame containing all cheaper alternatives.
    """
    category = row['Category']
    price = row['Price (PLN)']

    return dataframe[
        (dataframe['Category'] == category)
        & (dataframe['Price (PLN)'] < price)
    ]