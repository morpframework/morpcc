from morpfw.crud.storage.pgsqlstorage import PgSQLStorage

from ..app import App
from .model import EntityCollection, EntityModel

#
from .modelui import EntityCollectionUI, EntityModelUI

#
from .storage import EntityStorage


def get_collection(request):
    storage = EntityStorage(request)
    return EntityCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EntityCollection, path="/api/v1/entity")
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityModel, path="/api/v1/entity/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=EntityCollectionUI, path="/entity")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=EntityModelUI, path="/entity/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()
