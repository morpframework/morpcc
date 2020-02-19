from ..app import App
from .model import ApplicationModel, ApplicationCollection
# 
from .modelui import ApplicationModelUI, ApplicationCollectionUI
# 
from .storage import ApplicationStorage


def get_collection(request):
    storage = ApplicationStorage(request)
    return ApplicationCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ApplicationCollection,
          path='/api/v1/application')
def _get_collection(request):
    return get_collection(request)


@App.path(model=ApplicationModel,
          path='/api/v1/application/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return ApplicationCollectionUI(request, col)

@App.path(model=ApplicationCollectionUI,
          path='/application')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=ApplicationModelUI,
          path='/application/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
