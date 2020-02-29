from ..app import App
from .model import EndpointModel, EndpointCollection
# 
from .modelui import EndpointModelUI, EndpointCollectionUI
# 
from .storage import EndpointStorage


def get_collection(request):
    storage = EndpointStorage(request)
    return EndpointCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EndpointCollection,
          path='/api/v1/endpoint')
def _get_collection(request):
    return get_collection(request)


@App.path(model=EndpointModel,
          path='/api/v1/endpoint/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return EndpointCollectionUI(request, col)

@App.path(model=EndpointCollectionUI,
          path='/endpoint')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return EndpointModelUI(
        request, model,
        EndpointCollectionUI(request, col))

@App.path(model=EndpointModelUI,
          path='/endpoint/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
