from views.view import View
from components.component import Component
from components.default_components import defaults


home = View(name="home", route="/home")
home.add_component(defaults["STATISTICS_BAR"])
home.add_component(defaults["NAVIGATION_BAR"])
print(home)
