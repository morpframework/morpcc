from ..app import App
from .model import EntityValidatorAssignmentCollection, EntityValidatorAssignmentModel

#
from .modelui import (
    EntityValidatorAssignmentCollectionUI,
    EntityValidatorAssignmentModelUI,
)

#
from .storage import EntityValidatorAssignmentStorage


def get_collection(request):
    storage = EntityValidatorAssignmentStorage(request)
    return EntityValidatorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(
    model=EntityValidatorAssignmentCollection, path="/api/v1/entityvalidatorassignment"
)
def _get_collection(request):
    return get_collection(request)


@App.path(
    model=EntityValidatorAssignmentModel,
    path="/api/v1/entityvalidatorassignment/{identifier}",
)
def _get_model(request, identifier):
    return get_model(request, identifier)


#


@App.path(
    model=EntityValidatorAssignmentCollectionUI, path="/entityvalidatorassignment"
)
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(
    model=EntityValidatorAssignmentModelUI,
    path="/entityvalidatorassignment/{identifier}",
)
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
