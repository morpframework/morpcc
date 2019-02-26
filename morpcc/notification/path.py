from ..app import App
from .model import NotificationModel, NotificationCollection
#
from .modelui import NotificationModelUI, NotificationCollectionUI
#
from .storage import NotificationStorage


def get_collection(request):
    storage = NotificationStorage(request)
    return NotificationCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=NotificationCollection,
          path='/api/v1/notification')
def _get_collection(request):
    return get_collection(request)


@App.path(model=NotificationModel,
          path='/api/v1/notification/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

#


def get_collection_ui(request):
    col = get_collection(request)
    return NotificationCollectionUI(request, col)

@App.path(model=NotificationCollectionUI,
          path='/notification')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=NotificationModelUI,
          path='/notification/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
#
