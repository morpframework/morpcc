from ..app import App
from .model import EntityValidatorModel, EntityValidatorCollection

#
from .modelui import EntityValidatorModelUI, EntityValidatorCollectionUI

#
from .storage import EntityValidatorStorage


def get_collection(request):
    storage = EntityValidatorStorage(request)
    return EntityValidatorCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EntityValidatorCollection, path="/api/v1/entityvalidator")
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityValidatorModel, path="/api/v1/entityvalidator/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


#


def get_collection_ui(request):
    col = get_collection(request)
    return EntityValidatorCollectionUI(request, col)


@App.path(model=EntityValidatorCollectionUI, path="/entityvalidator")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)


@App.path(model=EntityValidatorModelUI, path="/entityvalidator/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#

