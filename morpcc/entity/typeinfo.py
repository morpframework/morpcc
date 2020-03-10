from ..app import App
from .model import EntityCollection, EntityModel

#
from .modelui import EntityCollectionUI, EntityModelUI
from .path import get_collection, get_model
from .schema import EntitySchema

#


@App.typeinfo(name="morpcc.entity", schema=EntitySchema)
def get_typeinfo(request):
    return {
        "title": "Entity",
        "description": "Entity type",
        "schema": EntitySchema,
        "collection": EntityCollection,
        "collection_factory": get_collection,
        "model": EntityModel,
        "model_factory": get_model,
        #
        "collection_ui": EntityCollectionUI,
        "model_ui": EntityModelUI,
        "internal": True
        #
    }
