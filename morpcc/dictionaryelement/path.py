from ..app import App
from .model import DictionaryElementCollection, DictionaryElementModel

#
from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI

#
from .storage import DictionaryElementStorage


def get_collection(request):
    storage = DictionaryElementStorage(request)
    return DictionaryElementCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DictionaryElementCollection, path="/api/v1/dictionaryelement")
def _get_collection(request):
    return get_collection(request)


@App.path(model=DictionaryElementModel, path="/api/v1/dictionaryelement/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


#


def get_collection_ui(request):
    col = get_collection(request)
    return DictionaryElementCollectionUI(request, col)


@App.path(model=DictionaryElementCollectionUI, path="/dictionaryelement")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return DictionaryElementModelUI(
        request, model, DictionaryElementCollectionUI(request, col)
    )


@App.path(model=DictionaryElementModelUI, path="/dictionaryelement/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)

#

