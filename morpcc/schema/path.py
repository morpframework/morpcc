from ..app import App
from .model import SchemaModel, SchemaCollection
# 
from .modelui import SchemaModelUI, SchemaCollectionUI
# 
from .storage import SchemaStorage


def get_collection(request):
    storage = SchemaStorage(request)
    return SchemaCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=SchemaCollection,
          path='/api/v1/schema')
def _get_collection(request):
    return get_collection(request)


@App.path(model=SchemaModel,
          path='/api/v1/schema/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return SchemaCollectionUI(request, col)

@App.path(model=SchemaCollectionUI,
          path='/schema')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return SchemaModelUI(
        request, model,
        SchemaCollectionUI(request, col))

@App.path(model=SchemaModelUI,
          path='/schema/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
