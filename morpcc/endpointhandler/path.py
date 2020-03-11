from ..app import App
from .model import EndpointHandlerModel, EndpointHandlerCollection
# 
from .modelui import EndpointHandlerModelUI, EndpointHandlerCollectionUI
# 
from .storage import EndpointHandlerStorage


def get_collection(request):
    storage = EndpointHandlerStorage(request)
    return EndpointHandlerCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EndpointHandlerCollection,
          path='/api/v1/endpointhandler')
def _get_collection(request):
    return get_collection(request)


@App.path(model=EndpointHandlerModel,
          path='/api/v1/endpointhandler/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


@App.path(model=EndpointHandlerCollectionUI,
          path='/endpointhandler')
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=EndpointHandlerModelUI,
          path='/endpointhandler/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

# 
