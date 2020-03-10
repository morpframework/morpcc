from webob.exc import HTTPNotFound

from ..app import App
from .model import ReferenceDataCollection, ReferenceDataModel

#
from .modelui import ReferenceDataCollectionUI, ReferenceDataModelUI

#
from .storage import ReferenceDataStorage


def get_collection(request):
    storage = ReferenceDataStorage(request)
    return ReferenceDataCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ReferenceDataCollection, path="/api/v1/referencedata")
def _get_collection(request):
    return get_collection(request)


@App.path(model=ReferenceDataModel, path="/api/v1/referencedata/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=ReferenceDataCollectionUI, path="/referencedata")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=ReferenceDataModelUI, path="/referencedata/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
