from ..app import App
from .model import AttributeModel, AttributeCollection
# 
from .modelui import AttributeModelUI, AttributeCollectionUI
# 
from .storage import AttributeStorage


def get_collection(request):
    storage = AttributeStorage(request)
    return AttributeCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=AttributeCollection,
          path='/api/v1/attribute')
def _get_collection(request):
    return get_collection(request)


@App.path(model=AttributeModel,
          path='/api/v1/attribute/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return AttributeCollectionUI(request, col)

@App.path(model=AttributeCollectionUI,
          path='/attribute')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=AttributeModelUI,
          path='/attribute/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
