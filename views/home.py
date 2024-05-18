from views.view import View
import utils.services as services
from utils.enums import FletNames
from components.component import Component, DefaultComponents


home = View(name=FletNames.HOME, route=f"/{FletNames.HOME}")
home.add_component(DefaultComponents.STATISTICS_BAR.value)
home.add_component(DefaultComponents.NAVIGATION_BAR.value)
home.log()
