from ..app import App
from .model import SettingModel, SettingCollection
# 
from .modelui import SettingModelUI, SettingCollectionUI
# 
from .storage import SettingStorage


def get_collection(request):
    storage = SettingStorage(request)
    return SettingCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=SettingCollection,
          path='/api/v1/setting')
def _get_collection(request):
    return get_collection(request)


@App.path(model=SettingModel,
          path='/api/v1/setting/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


def get_collection_ui(request):
    col = get_collection(request)
    return SettingCollectionUI(request, col)

@App.path(model=SettingCollectionUI,
          path='/site-settings/setting')
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)

@App.path(model=SettingModelUI,
          path='/site-settings/setting/{identifier}')
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)
# 
