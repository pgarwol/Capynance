from views.view import View, ViewsInitialStates
import utils.services as services
from utils.enums import FletNames
from components.component import Component, DefaultComponents
import flet as ft


finances = View(name=FletNames.FINANCES, route=f"/{FletNames.FINANCES}")
finances.add_component(DefaultComponents.STATISTICS_BAR.value)
finances.add_component(
    Component(
        content=[
            ft.Image(
                src="https://img.freepik.com/premium-wektory/happy-piggy-bank-maskotka-design_35422-31.jpg?w=1060"
            ),
            ft.Text("Amount"),
        ],
        description="Money box",
    )
)
finances.add_component(
    Component(
        content=[
            ft.Text("Spendings"),
        ],
        description="User's spendings",
    )
)
finances.add_component(DefaultComponents.NAVIGATION_BAR.value)
ViewsInitialStates.set_finances_copy(finances)
finances.log()
