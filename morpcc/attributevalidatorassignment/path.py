from ..app import App
from .model import AttributeValidatorAssignmentModel, AttributeValidatorAssignmentCollection
# 
from .modelui import AttributeValidatorAssignmentModelUI, AttributeValidatorAssignmentCollectionUI
# 
from .storage import AttributeValidatorAssignmentStorage


def get_collection(request):
    storage = AttributeValidatorAssignmentStorage(request)
    return AttributeValidatorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=AttributeValidatorAssignmentCollection,
          path='/api/v1/attributevalidatorassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=AttributeValidatorAssignmentModel,
          path='/api/v1/attributevalidatorassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return AttributeValidatorAssignmentCollectionUI(request, col)

@App.path(model=AttributeValidatorAssignmentCollectionUI,
          path='/attributevalidatorassignment')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return AttributeValidatorAssignmentModelUI(
        request, model,
        AttributeValidatorAssignmentCollectionUI(request, col))

@App.path(model=AttributeValidatorAssignmentModelUI,
          path='/attributevalidatorassignment/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
