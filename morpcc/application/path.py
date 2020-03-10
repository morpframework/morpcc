from ..app import App
from .model import ApplicationCollection, ApplicationModel

#
from .modelui import ApplicationCollectionUI, ApplicationModelUI

#
from .storage import ApplicationStorage


def get_collection(request):
    storage = ApplicationStorage(request)
    return ApplicationCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ApplicationCollection, path="/api/v1/application")
def _get_collection(request):
    return get_collection(request)


@App.path(model=ApplicationModel, path="/api/v1/application/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=ApplicationCollectionUI, path="/application")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=ApplicationModelUI, path="/application/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
