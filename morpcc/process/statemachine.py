import morpfw

from ..app import App
from .model import ProcessModel


class ProcessStateMachine(morpfw.StateMachine):

    states = ["new", "running", "cancelled", "failed", "success"]
    transitions = [
        {"trigger": "start", "source": "new", "dest": "running"},
        {"trigger": "cancel", "source": "running", "dest": "cancelled"},
        {"trigger": "fail", "source": "running", "dest": "failed"},
        {"trigger": "complete", "source": "running", "dest": "success"},
    ]

    protected_transitions = ["fail", "complete"]


@App.statemachine(model=ProcessModel)
def get_statemachine(context):
    return ProcessStateMachine(context)
