from components.default_components import default_components
from components.component import Component
from views.view import View


main_screen = View(route="/")
main_screen.add_component(default_components["STATS"])
main_screen.add_component(default_components["NAVIGATION"])
