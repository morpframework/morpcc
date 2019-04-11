from ..app import App, SQLAuthApp
from morpfw.authn.pas.user.model import UserModel
from dataclasses import dataclass
import morpfw


class UserStateMachine(morpfw.StateMachine):

    states = ['new', 'active', 'inactive']
    transitions = [
        {'trigger': 'initialize', 'source': 'new', 'dest': 'active'},
        {'trigger': 'activate', 'source': 'inactive', 'dest': 'active'},
        {'trigger': 'deactivate', 'source': 'active', 'dest': 'inactive'},
    ]


@SQLAuthApp.statemachine(model=UserModel)
def userstatemachine(context):
    return UserStateMachine(context)
