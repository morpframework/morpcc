from ..app import App
from .model import EntityConstraintModel, EntityConstraintCollection
# 
from .modelui import EntityConstraintModelUI, EntityConstraintCollectionUI
# 
from .storage import EntityConstraintStorage


def get_collection(request):
    storage = EntityConstraintStorage(request)
    return EntityConstraintCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EntityConstraintCollection,
          path='/api/v1/entityconstraint')
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityConstraintModel,
          path='/api/v1/entityconstraint/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return EntityConstraintCollectionUI(request, col)

@App.path(model=EntityConstraintCollectionUI,
          path='/entityconstraint')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=EntityConstraintModelUI,
          path='/entityconstraint/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
