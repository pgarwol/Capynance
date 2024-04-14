from components.default_components import defaults
from components.component import Component
from views.view import View


main_screen = View(name="Main Screen", route="/")
main_screen.add_component(defaults["STATS"])
main_screen.add_component(defaults["NAVIGATION"])
print(main_screen)
