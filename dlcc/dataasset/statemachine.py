import morpfw
from .model import DataAssetModel
from ..app import App


class DataAssetStateMachine(morpfw.StateMachine):
    states = ['new', 'approved', 'rejected']

    transitions = [
        {'trigger': 'approve', 'source': 'new', 'dest': 'approved'},
        {'trigger': 'reject', 'source': 'new', 'dest': 'rejected'},
    ]


@App.statemachine(model=DataAssetModel)
def get_dataasset_statemachine(obj):
    return DataAssetStateMachine(obj)
