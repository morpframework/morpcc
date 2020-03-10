from ..app import App
from .model import DictionaryEntityCollection, DictionaryEntityModel
#
from .modelui import DictionaryEntityCollectionUI, DictionaryEntityModelUI
#
from .storage import DictionaryEntityStorage


def get_collection(request):
    storage = DictionaryEntityStorage(request)
    return DictionaryEntityCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DictionaryEntityCollection, path="/api/v1/dictionaryentity")
def _get_collection(request):
    return get_collection(request)


@App.path(model=DictionaryEntityModel, path="/api/v1/dictionaryentity/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=DictionaryEntityCollectionUI, path="/dictionaryentity")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=DictionaryEntityModelUI, path="/dictionaryentity/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#
