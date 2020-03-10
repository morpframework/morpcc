from ..app import App
from .model import (
    ApplicationBehaviorAssignmentCollection,
    ApplicationBehaviorAssignmentModel,
)

#
from .modelui import (
    ApplicationBehaviorAssignmentCollectionUI,
    ApplicationBehaviorAssignmentModelUI,
)

#
from .storage import ApplicationBehaviorAssignmentStorage


def get_collection(request):
    storage = ApplicationBehaviorAssignmentStorage(request)
    return ApplicationBehaviorAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(
    model=ApplicationBehaviorAssignmentCollection,
    path="/api/v1/applicationbehaviorassignment",
)
def _get_collection(request):
    return get_collection(request)


@App.path(
    model=ApplicationBehaviorAssignmentModel,
    path="/api/v1/applicationbehaviorassignment/{identifier}",
)
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(
    model=ApplicationBehaviorAssignmentCollectionUI,
    path="/applicationbehaviorassignment",
)
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(
    model=ApplicationBehaviorAssignmentModelUI,
    path="/applicationbehaviorassignment/{identifier}",
)
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
