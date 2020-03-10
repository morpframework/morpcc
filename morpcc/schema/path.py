from ..app import App
from .model import SchemaCollection, SchemaModel
# 
from .modelui import SchemaCollectionUI, SchemaModelUI
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



@App.path(model=SchemaCollectionUI,
          path='/schema')
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()

@App.path(model=SchemaModelUI,
          path='/schema/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()
# 
