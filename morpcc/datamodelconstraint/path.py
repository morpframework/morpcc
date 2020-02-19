from ..app import App
from .model import DataModelConstraintModel, DataModelConstraintCollection
# 
from .modelui import DataModelConstraintModelUI, DataModelConstraintCollectionUI
# 
from .storage import DataModelConstraintStorage


def get_collection(request):
    storage = DataModelConstraintStorage(request)
    return DataModelConstraintCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DataModelConstraintCollection,
          path='/api/v1/datamodelconstraint')
def _get_collection(request):
    return get_collection(request)


@App.path(model=DataModelConstraintModel,
          path='/api/v1/datamodelconstraint/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return DataModelConstraintCollectionUI(request, col)

@App.path(model=DataModelConstraintCollectionUI,
          path='/datamodelconstraint')
def _get_collection_ui(request):
    return get_collection_ui(request)

def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=DataModelConstraintModelUI,
          path='/datamodelconstraint/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
