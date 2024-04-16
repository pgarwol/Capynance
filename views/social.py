from components.default_components import defaults
from components.component import Component
from views.view import View
import flet as ft


social = View(name="Social", route="/social")
social.add_component(defaults["STATS"])
social.add_component(
    Component(content=[ft.Text("Friends")], description="Friends")
)
social.add_component(defaults["NAVIGATION"])