from ..app import App
from .model import ApplicationBehaviorAssignmentModel, ApplicationBehaviorAssignmentCollection
# 
from .modelui import ApplicationBehaviorAssignmentModelUI, ApplicationBehaviorAssignmentCollectionUI
# 
from .storage import ApplicationBehaviorAssignmentStorage


def get_collection(request):
    storage = ApplicationBehaviorAssignmentStorage(request)
    return ApplicationBehaviorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ApplicationBehaviorAssignmentCollection,
          path='/api/v1/applicationbehaviorassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=ApplicationBehaviorAssignmentModel,
          path='/api/v1/applicationbehaviorassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return ApplicationBehaviorAssignmentCollectionUI(request, col)

@App.path(model=ApplicationBehaviorAssignmentCollectionUI,
          path='/applicationbehaviorassignment')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return ApplicationBehaviorAssignmentModelUI(
        request, model,
        ApplicationBehaviorAssignmentCollectionUI(request, col))

@App.path(model=ApplicationBehaviorAssignmentModelUI,
          path='/applicationbehaviorassignment/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
