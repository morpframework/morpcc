from morpfw.crud.storage.pgsqlstorage import PgSQLStorage

from ..app import App
from .model import (
    EntityCollection,
    EntityContentCollection,
    EntityContentModel,
    EntityModel,
)

#
from .modelui import (
    EntityCollectionUI,
    EntityContentCollectionUI,
    EntityContentModelUI,
    EntityModelUI,
)

#
from .storage import EntityStorage


def get_collection(request):
    storage = EntityStorage(request)
    return EntityCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


def get_collection_ui(request):
    return get_collection(request).ui()


def get_model_ui(request, identifier):
    return get_collection_ui(request).get(identifier)


@App.path(model=EntityCollection, path="/api/v1/entity")
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityModel, path="/api/v1/entity/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(
    model=EntityContentCollection,
    path="/api/v1/entity/{identifier}/records",
    variables=lambda obj: {"identifier": obj.__parent__.identifier,},
)
def _get_content_collection(request, identifier):
    dm = get_model(request, identifier)
    return dm.content_collection()


@App.path(
    model=EntityContentModel,
    path="/api/v1/entity/{identifier}/records/{recordidentifier}",
    variables=lambda obj: {
        "identifier": obj.collection.__parent__.identifier,
        "recordidentifier": obj.identifier,
    },
)
def _get_content_model(request, identifier, recordidentifier):
    dm = get_model(request, identifier)
    col = dm.content_collection()
    return col.get(recordidentifier)


#


@App.path(model=EntityCollectionUI, path="/entity")
def _get_collection_ui(request):
    return get_collection(request).ui()


def get_model_ui(request, identifier):
    col = get_collection(request).ui()
    return col.get(identifier)


@App.path(model=EntityModelUI, path="/entity/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#
DATA = {}


def _get_model_content_collection_ui(parent, request):
    col = parent.content_collection()
    return col.ui()


@App.path(
    model=EntityContentCollectionUI,
    path="/entity/{identifier}/records/",
    variables=lambda obj: {"identifier": obj.collection.__parent__.identifier},
)
def get_model_content_collection_ui(request, identifier):
    parent = get_model(request, identifier)
    return _get_model_content_collection_ui(parent, request)


@App.path(
    model=EntityContentModelUI,
    path="/entity/{identifier}/records/{recordidentifier}",
    variables=lambda obj: {
        "identifier": obj.collection_ui.collection.__parent__.identifier,
        "recordidentifier": obj.model.identifier,
    },
)
def get_model_content_model(request, identifier, recordidentifier):
    parent = get_model(request, identifier)
    col = _get_model_content_collection_ui(parent, request)
    return col.get(recordidentifier)
