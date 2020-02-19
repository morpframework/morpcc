from ..app import App
from .model import AttributeConstraintModel, AttributeConstraintCollection

#
from .modelui import AttributeConstraintModelUI, AttributeConstraintCollectionUI

#
from .storage import AttributeConstraintStorage


def get_collection(request):
    storage = AttributeConstraintStorage(request)
    return AttributeConstraintCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=AttributeConstraintCollection, path="/api/v1/attributeconstraint")
def _get_collection(request):
    return get_collection(request)


@App.path(
    model=AttributeConstraintModel, path="/api/v1/attributeconstraint/{identifier}"
)
def _get_model(request, identifier):
    return get_model(request, identifier)


#


def get_collection_ui(request):
    col = get_collection(request)
    return AttributeConstraintCollectionUI(request, col)


@App.path(model=AttributeConstraintCollectionUI, path="/attributeconstraint")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)


@App.path(model=AttributeConstraintModelUI, path="/attributeconstraint/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#

