from ..app import App
from .model import RelationshipCollection, RelationshipModel

#
from .modelui import RelationshipCollectionUI, RelationshipModelUI

#
from .storage import RelationshipStorage


def get_collection(request):
    storage = RelationshipStorage(request)
    return RelationshipCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=RelationshipCollection, path="/api/v1/relationship")
def _get_collection(request):
    return get_collection(request)


@App.path(model=RelationshipModel, path="/api/v1/relationship/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=RelationshipCollectionUI, path="/relationship")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=RelationshipModelUI, path="/relationship/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

