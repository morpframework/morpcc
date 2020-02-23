from ..app import App
from .model import DictionaryEntityModel, DictionaryEntityCollection
# 
from .modelui import DictionaryEntityModelUI, DictionaryEntityCollectionUI
# 
from .storage import DictionaryEntityStorage


def get_collection(request):
    storage = DictionaryEntityStorage(request)
    return DictionaryEntityCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DictionaryEntityCollection,
          path='/api/v1/dictionaryentity')
def _get_collection(request):
    return get_collection(request)


@App.path(model=DictionaryEntityModel,
          path='/api/v1/dictionaryentity/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return DictionaryEntityCollectionUI(request, col)

@App.path(model=DictionaryEntityCollectionUI,
          path='/dictionaryentity')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return DictionaryEntityModelUI(
        request, model,
        DictionaryEntityCollectionUI(request, col))

@App.path(model=DictionaryEntityModelUI,
          path='/dictionaryentity/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
