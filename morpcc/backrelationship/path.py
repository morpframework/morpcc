from ..app import App
from .model import BackRelationshipCollection, BackRelationshipModel

#
from .modelui import BackRelationshipCollectionUI, BackRelationshipModelUI

#
from .storage import BackRelationshipStorage


def get_collection(request):
    storage = BackRelationshipStorage(request)
    return BackRelationshipCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=BackRelationshipCollection, path="/api/v1/backrelationship")
def _get_collection(request):
    return get_collection(request)


@App.path(model=BackRelationshipModel, path="/api/v1/backrelationship/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=BackRelationshipCollectionUI, path="/backrelationship")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=BackRelationshipModelUI, path="/backrelationship/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

