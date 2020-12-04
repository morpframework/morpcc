import morpfw

from ..app import App
from .model import ApplicationModel


class ApplicationStateMachine(morpfw.StateMachine):

    states = ["active", "upgrading", "pending_delete", "deleting"]

    transitions = [
        {"trigger": "delete", "source": "active", "dest": "pending_delete",},
        {"trigger": "process_delete", "source": "pending_delete", "dest": "deleting"},
        {"trigger": "upgrade", "source": "active", "dest": "upgrading"},
        {"trigger": "upgrade_complete", "source": "upgrading", "dest": "active"},
    ]

    def on_enter_upgrading(self):
        context = self._context
        request = self._request
        request.async_dispatch("morpcc.upgrade_application", app_name=context["name"])


@App.statemachine(model=ApplicationModel)
def get_statemachine(context):
    return ApplicationStateMachine(context)
