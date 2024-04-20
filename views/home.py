from components.default_components import defaults
from components.component import Component
from views.view import View


home = View(name="Main Screen", route="/")
home.add_component(defaults["STATISTICS_BAR"])
home.add_component(defaults["NAVIGATION_BAR"])
print(home)
