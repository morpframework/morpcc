from morpfw.crud.storage.pgsqlstorage import PgSQLStorage

from ..app import App
from .model import (
    DataModelCollection,
    DataModelContentCollection,
    DataModelContentModel,
    DataModelModel,
)

#
from .modelui import (
    DataModelCollectionUI,
    DataModelContentCollectionUI,
    DataModelContentModelUI,
    DataModelModelUI,
)

#
from .storage import DataModelStorage


def get_collection(request):
    storage = DataModelStorage(request)
    return DataModelCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=DataModelCollection, path="/api/v1/datamodel")
def _get_collection(request):
    return get_collection(request)


@App.path(model=DataModelModel, path="/api/v1/datamodel/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(
    model=DataModelContentCollection,
    path="/api/v1/datamodel/{identifier}/records",
    variables=lambda obj: {"identifier": obj.__parent__.identifier,},
)
def _get_content_collection(request, identifier):
    dm = get_model(request, identifier)
    return dm.content_collection()


@App.path(
    model=DataModelContentModel,
    path="/api/v1/datamodel/{identifier}/records/{recordidentifier}",
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


def get_collection_ui(request):
    col = get_collection(request)
    return DataModelCollectionUI(request, col)


@App.path(model=DataModelCollectionUI, path="/datamodel")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection_ui(request)
    return col.get(identifier)


@App.path(model=DataModelModelUI, path="/datamodel/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#
DATA = {}


def _get_model_content_collection_ui(parent, request):
    col = parent.content_collection()
    return DataModelContentCollectionUI(request, col)


@App.path(
    model=DataModelContentCollectionUI,
    path="/datamodel/{identifier}/records/",
    variables=lambda obj: {"identifier": obj.collection.__parent__.identifier},
)
def get_model_content_collection_ui(request, identifier):
    parent = get_model(request, identifier)
    return _get_model_content_collection_ui(parent, request)


@App.path(
    model=DataModelContentModelUI,
    path="/datamodel/{identifier}/records/{recordidentifier}",
    variables=lambda obj: {
        "identifier": obj.collection_ui.collection.__parent__.identifier,
        "recordidentifier": obj.model.identifier,
    },
)
def get_model_content_model(request, identifier, recordidentifier):
    parent = get_model(request, identifier)
    col = _get_model_content_collection_ui(parent, request)
    return col.get(recordidentifier)
