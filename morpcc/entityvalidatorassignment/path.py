from ..app import App
from .model import EntityValidatorAssignmentModel, EntityValidatorAssignmentCollection
# 
from .modelui import EntityValidatorAssignmentModelUI, EntityValidatorAssignmentCollectionUI
# 
from .storage import EntityValidatorAssignmentStorage


def get_collection(request):
    storage = EntityValidatorAssignmentStorage(request)
    return EntityValidatorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EntityValidatorAssignmentCollection,
          path='/api/v1/entityvalidatorassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityValidatorAssignmentModel,
          path='/api/v1/entityvalidatorassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return EntityValidatorAssignmentCollectionUI(request, col)

@App.path(model=EntityValidatorAssignmentCollectionUI,
          path='/entityvalidatorassignment')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return EntityValidatorAssignmentModelUI(
        request, model,
        EntityValidatorAssignmentCollectionUI(request, col))

@App.path(model=EntityValidatorAssignmentModelUI,
          path='/entityvalidatorassignment/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
