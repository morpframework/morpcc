from ..app import App
from .model import DictionaryElementValidatorAssignmentModel, DictionaryElementValidatorAssignmentCollection
# 
from .modelui import DictionaryElementValidatorAssignmentModelUI, DictionaryElementValidatorAssignmentCollectionUI
# 
from .storage import DictionaryElementValidatorAssignmentStorage


def get_collection(request):
    storage = DictionaryElementValidatorAssignmentStorage(request)
    return DictionaryElementValidatorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DictionaryElementValidatorAssignmentCollection,
          path='/api/v1/dictionaryelementvalidatorassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=DictionaryElementValidatorAssignmentModel,
          path='/api/v1/dictionaryelementvalidatorassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return DictionaryElementValidatorAssignmentCollectionUI(request, col)

@App.path(model=DictionaryElementValidatorAssignmentCollectionUI,
          path='/dictionaryelementvalidatorassignment')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return DictionaryElementValidatorAssignmentModelUI(
        request, model,
        DictionaryElementValidatorAssignmentCollectionUI(request, col))

@App.path(model=DictionaryElementValidatorAssignmentModelUI,
          path='/dictionaryelementvalidatorassignment/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
