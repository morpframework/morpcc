import rulez

from ..app import App
from .model import (
    EndpointCollection,
    EndpointModel,
    NamedEndpointCollection,
    NamedEndpointModel,
)

#
from .modelui import EndpointCollectionUI, EndpointModelUI

#
from .storage import EndpointStorage


def get_collection(request):
    storage = EndpointStorage(request)
    return EndpointCollection(request, storage)


def get_named_collection(request):
    storage = EndpointStorage(request)
    storage.model = NamedEndpointModel
    return NamedEndpointCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


def get_named_model(request, identifier):
    col = get_named_collection(request)
    items = col.search(rulez.field["name"] == identifier)
    if items:
        return items[0]
    return None


@App.path(model=EndpointCollection, path="/api/v1/endpoint")
def _get_collection(request):
    return get_collection(request)


@App.path(model=EndpointModel, path="/api/v1/endpoint/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=NamedEndpointCollection, path="/api/v1/endpoint/by_name/")
def _get_named_collection(request):
    return get_named_collection(request)


@App.path(model=NamedEndpointModel, path="/api/v1/endpoint/by_name/{identifier}")
def _get_named_model(request, identifier):
    return get_named_model(request, identifier)


#


def get_collection_ui(request):
    col = get_collection(request)
    return EndpointCollectionUI(request, col)


@App.path(model=EndpointCollectionUI, path="/endpoint")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return EndpointModelUI(request, model, EndpointCollectionUI(request, col))


@App.path(model=EndpointModelUI, path="/endpoint/{identifier}")
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#
