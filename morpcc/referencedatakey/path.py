from ..app import App
from .model import ReferenceDataKeyCollection, ReferenceDataKeyModel

#
from .modelui import ReferenceDataKeyCollectionUI, ReferenceDataKeyModelUI

#
from .storage import ReferenceDataKeyStorage


def get_collection(request):
    storage = ReferenceDataKeyStorage(request)
    return ReferenceDataKeyCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ReferenceDataKeyCollection, path="/api/v1/referencedatakey")
def _get_collection(request):
    return get_collection(request)


@App.path(model=ReferenceDataKeyModel, path="/api/v1/referencedatakey/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=ReferenceDataKeyCollectionUI, path="/referencedatakey")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=ReferenceDataKeyModelUI, path="/referencedatakey/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

