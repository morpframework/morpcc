from ..app import App
from .model import EndpointCollection, EndpointModel

#
from .modelui import EndpointCollectionUI, EndpointModelUI
from .path import get_collection, get_model
from .schema import EndpointSchema

#


@App.typeinfo(name="morpcc.endpoint", schema=EndpointSchema)
def get_typeinfo(request):
    return {
        "title": "Endpoint",
        "description": "Endpoint type",
        "schema": EndpointSchema,
        "collection": EndpointCollection,
        "collection_factory": get_collection,
        "model": EndpointModel,
        "model_factory": get_model,
        #
        "collection_ui": EndpointCollectionUI,
        "model_ui": EndpointModelUI,
        "internal": True,
        #
    }
