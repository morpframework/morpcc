from ..app import App
from .model import ReferenceEntity, ReferenceDataCollection
#
from .modelui import ReferenceEntityUI, ReferenceDataCollectionUI
#
from .storage import ReferenceDataStorage
from webob.exc import HTTPNotFound


def get_collection(request):
    storage = ReferenceDataStorage(request)
    return ReferenceDataCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ReferenceDataCollection,
          path='/api/v1/referencedata')
def _get_collection(request):
    return get_collection(request)


@App.path(model=ReferenceEntity,
          path='/api/v1/referencedata/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

#


def get_collection_ui(request):
    col = get_collection(request)
    return ReferenceDataCollectionUI(request, col)

@App.path(model=ReferenceDataCollectionUI,
          path='/referencedata')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    if model is None:
        return None
    return ReferenceEntityUI(
        request, model,
        ReferenceDataCollectionUI(request, col))

@App.path(model=ReferenceEntityUI,
          path='/referencedata/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
#
