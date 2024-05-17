import json
from pathlib import Path

_PRODUCT_DATABASE_NAME = "shop_database.json"


class Product:
    def __init__(self, id, name, images, price):
        self.id = id
        self.name = name
        self.images = images
        self.price = price


def read_product_from_db(product_id: str) -> Product:
    """
    Reads product data from the database based on the provided ID.

    Args:
        product_id (str): The ID of the product to read from the database.

    Returns:
        Product: The product created from the retrieved data.
    """
    with open(Path("./database/shop_database.json").resolve(), encoding="utf-8") as db:
        product_data = json.load(db)[product_id]

    return Product(
        id=product_id,
        name=product_data["name"],
        images=product_data["images"],
        price=product_data["price"],
    )
