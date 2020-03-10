from ..app import App
from .model import ApplicationCollection, ApplicationModel

#
from .modelui import ApplicationCollectionUI, ApplicationModelUI
from .path import get_collection, get_model
from .schema import ApplicationSchema

#


@App.typeinfo(name="morpcc.application", schema=ApplicationSchema)
def get_typeinfo(request):
    return {
        "title": "Application",
        "description": "Application type",
        "schema": ApplicationSchema,
        "collection": ApplicationCollection,
        "collection_factory": get_collection,
        "model": ApplicationModel,
        "model_factory": get_model,
        #
        "collection_ui": ApplicationCollectionUI,
        "model_ui": ApplicationModelUI,
        "internal": True
        #
    }
