from ..app import App
from .model import BehaviorAssignmentCollection, BehaviorAssignmentModel

#
from .modelui import BehaviorAssignmentCollectionUI, BehaviorAssignmentModelUI

#
from .storage import BehaviorAssignmentStorage


def get_collection(request):
    storage = BehaviorAssignmentStorage(request)
    return BehaviorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=BehaviorAssignmentCollection, path="/api/v1/behaviorassignment")
def _get_collection(request):
    return get_collection(request)


@App.path(model=BehaviorAssignmentModel, path="/api/v1/behaviorassignment/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=BehaviorAssignmentCollectionUI, path="/behaviorassignment")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=BehaviorAssignmentModelUI, path="/behaviorassignment/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
