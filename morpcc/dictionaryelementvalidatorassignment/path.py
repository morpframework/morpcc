from ..app import App
from .model import (
    DictionaryElementValidatorAssignmentCollection,
    DictionaryElementValidatorAssignmentModel,
)

#
from .modelui import (
    DictionaryElementValidatorAssignmentCollectionUI,
    DictionaryElementValidatorAssignmentModelUI,
)

#
from .storage import DictionaryElementValidatorAssignmentStorage


def get_collection(request):
    storage = DictionaryElementValidatorAssignmentStorage(request)
    return DictionaryElementValidatorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(
    model=DictionaryElementValidatorAssignmentCollection,
    path="/api/v1/dictionaryelementvalidatorassignment",
)
def _get_collection(request):
    return get_collection(request)


@App.path(
    model=DictionaryElementValidatorAssignmentModel,
    path="/api/v1/dictionaryelementvalidatorassignment/{identifier}",
)
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(
    model=DictionaryElementValidatorAssignmentCollectionUI,
    path="/dictionaryelementvalidatorassignment",
)
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(
    model=DictionaryElementValidatorAssignmentModelUI,
    path="/dictionaryelementvalidatorassignment/{identifier}",
)
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

