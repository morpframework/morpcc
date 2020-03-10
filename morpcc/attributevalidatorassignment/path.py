from ..app import App
from .model import (
    AttributeValidatorAssignmentCollection,
    AttributeValidatorAssignmentModel,
)

#
from .modelui import (
    AttributeValidatorAssignmentCollectionUI,
    AttributeValidatorAssignmentModelUI,
)

#
from .storage import AttributeValidatorAssignmentStorage


def get_collection(request):
    storage = AttributeValidatorAssignmentStorage(request)
    return AttributeValidatorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(
    model=AttributeValidatorAssignmentCollection,
    path="/api/v1/attributevalidatorassignment",
)
def _get_collection(request):
    return get_collection(request)


@App.path(
    model=AttributeValidatorAssignmentModel,
    path="/api/v1/attributevalidatorassignment/{identifier}",
)
def _get_model(request, identifier):
    return get_model(request, identifier)


#


@App.path(
    model=AttributeValidatorAssignmentCollectionUI, path="/attributevalidatorassignment"
)
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(
    model=AttributeValidatorAssignmentModelUI,
    path="/attributevalidatorassignment/{identifier}",
)
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

