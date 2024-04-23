from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


shop = View(name="Shop", route="/shop")
shop.add_component(defaults["STATISTICS_BAR"])
shop.add_component(Component([ft.Text("SKLEP")], "View representing Shop."))
shop.add_component(defaults["NAVIGATION_BAR"])
print(shop)
