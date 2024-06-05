import pandas as pd
from utils.enums import DBFields
from pathlib import Path

products = pd.read_csv(Path(DBFields.RELATIVE_DB_PATH + "products_with_categories.csv").resolve())

subgroups_dict = {}
for category, group in products.groupby('Category'):
    sorted_group = group.sort_values(by='Price (PLN)')
    subgroups_dict[category] = sorted_group


def get_cheaper_alternatives(product_name: str, dataframe: pd.DataFrame) -> dict:
    """
    Returns all cheaper alternatives for a given row in the DataFrame.

    Parameters:
    product_name (str): Name of the product.
    dataframe (pd.DataFrame): The DataFrame to search within.

    Returns:
    dict: A dictionary containing all cheaper alternatives.
    """
    if product_name not in dataframe['Product'].values:
        print(f'Product has not been found: {product_name}')
        return {}

    row = dataframe.loc[dataframe['Product'] == product_name]

    category = row.iloc[0]['Category']
    price = row.iloc[0]['Price (PLN)']

    cheaper_products = dataframe[
        (dataframe['Category'] == category)
        & (dataframe['Price (PLN)'] < price)
        ]

    alternatives = {}
    for i, row_alternatives in cheaper_products.iterrows():
        alternatives[i] = {
            'Product': row_alternatives['Product'],
            'Price (PLN)': row_alternatives['Price (PLN)']
        }
    return alternatives
