from ..app import App
from .model import SelectionAttributeModel, SelectionAttributeCollection
# 
from .modelui import SelectionAttributeModelUI, SelectionAttributeCollectionUI
# 
from .storage import SelectionAttributeStorage


def get_collection(request):
    storage = SelectionAttributeStorage(request)
    return SelectionAttributeCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=SelectionAttributeCollection,
          path='/api/v1/selectionattribute')
def _get_collection(request):
    return get_collection(request)


@App.path(model=SelectionAttributeModel,
          path='/api/v1/selectionattribute/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return SelectionAttributeCollectionUI(request, col)

@App.path(model=SelectionAttributeCollectionUI,
          path='/selectionattribute')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return SelectionAttributeModelUI(
        request, model,
        SelectionAttributeCollectionUI(request, col))

@App.path(model=SelectionAttributeModelUI,
          path='/selectionattribute/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
