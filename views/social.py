from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


social = View(name="social", route="/social")
social.add_component(defaults["STATISTICS_BAR"])
social.add_component(Component([ft.Text("ZIOMKI")], "View representing Social."))
social.add_component(defaults["NAVIGATION_BAR"])
print(social)
