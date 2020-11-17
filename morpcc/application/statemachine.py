import morpfw

from ..app import App
from .model import ApplicationModel


class ApplicationStateMachine(morpfw.StateMachine):

    states = ["active", "pending_delete", "deleting"]

    transitions = [
        {
            "trigger": "delete",
            "source": "active",
            "dest": "pending_delete",
        },
        {"trigger": "process_delete", "source": "pending_delete", "dest": "deleting"},
    ]


@App.statemachine(model=ApplicationModel)
def get_statemachine(context):
    return ApplicationStateMachine(context)
