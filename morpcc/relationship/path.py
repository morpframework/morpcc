from ..app import App
from .model import RelationshipModel, RelationshipCollection
# 
from .modelui import RelationshipModelUI, RelationshipCollectionUI
# 
from .storage import RelationshipStorage


def get_collection(request):
    storage = RelationshipStorage(request)
    return RelationshipCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=RelationshipCollection,
          path='/api/v1/relationship')
def _get_collection(request):
    return get_collection(request)


@App.path(model=RelationshipModel,
          path='/api/v1/relationship/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return RelationshipCollectionUI(request, col)

@App.path(model=RelationshipCollectionUI,
          path='/relationship')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=RelationshipModelUI,
          path='/relationship/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
