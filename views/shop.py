from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


shop = View(name="Shop", route="/shop")
shop.add_component(defaults["STATS"])
shop.add_component(
    Component(content=[ft.Text("ITEMKI DO KUPIENI IŁOIŁO")], description="Items to buy")
)
shop.add_component(defaults["NAVIGATION"])
print(shop)
