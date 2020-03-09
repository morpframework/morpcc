from ..app import App
from .model import AttributeValidatorModel, AttributeValidatorCollection

#
from .modelui import AttributeValidatorModelUI, AttributeValidatorCollectionUI

#
from .storage import AttributeValidatorStorage


def get_collection(request):
    storage = AttributeValidatorStorage(request)
    return AttributeValidatorCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=AttributeValidatorCollection, path="/api/v1/attributevalidator")
def _get_collection(request):
    return get_collection(request)


@App.path(model=AttributeValidatorModel, path="/api/v1/attributevalidator/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


#


def get_collection_ui(request):
    col = get_collection(request)
    return AttributeValidatorCollectionUI(request, col)


@App.path(model=AttributeValidatorCollectionUI, path="/attributevalidator")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)


@App.path(model=AttributeValidatorModelUI, path="/attributevalidator/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#

