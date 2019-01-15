from ..app import App
from .model import DataAssetModel, DataAssetCollection
from .modelui import DataAssetModelUI, DataAssetCollectionUI
from .storage import DataAssetStorage


def get_collection(request):
    storage = DataAssetStorage(request)
    return DataAssetCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DataAssetCollection, path='/api/v1/dataasset')
def _get_collection(request):
    return get_collection(request)


@App.path(model=DataAssetModel, path='/api/v1/dataasset/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=DataAssetCollectionUI, path='/dataasset')
def get_collection_ui(request):
    col = get_collection(request)
    return DataAssetCollectionUI(request, col)


@App.path(model=DataAssetModelUI, path='/dataasset/{identifier}')
def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return DataAssetModelUI(request, model, DataAssetCollectionUI(request, col))
