from ..app import App
from .model import IndexModel, IndexCollection
# 
from .modelui import IndexModelUI, IndexCollectionUI
# 
from .storage import IndexStorage


def get_collection(request):
    storage = IndexStorage(request)
    return IndexCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=IndexCollection,
          path='/api/v1/index')
def _get_collection(request):
    return get_collection(request)


@App.path(model=IndexModel,
          path='/api/v1/index/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return IndexCollectionUI(request, col)

@App.path(model=IndexCollectionUI,
          path='/index')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=IndexModelUI,
          path='/index/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
