from ..app import App
from .model import BackRelationshipModel, BackRelationshipCollection
# 
from .modelui import BackRelationshipModelUI, BackRelationshipCollectionUI
# 
from .storage import BackRelationshipStorage


def get_collection(request):
    storage = BackRelationshipStorage(request)
    return BackRelationshipCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=BackRelationshipCollection,
          path='/api/v1/backrelationship')
def _get_collection(request):
    return get_collection(request)


@App.path(model=BackRelationshipModel,
          path='/api/v1/backrelationship/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return BackRelationshipCollectionUI(request, col)

@App.path(model=BackRelationshipCollectionUI,
          path='/backrelationship')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=BackRelationshipModelUI,
          path='/backrelationship/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
