from ..app import App
from .model import EntityCollection, EntityModel

#
from .modelui import EntityCollectionUI, EntityModelUI
from .path import get_collection, get_collection_ui, get_model, get_model_ui
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
        "collection_ui_factory": get_collection_ui,
        "model_ui": EntityModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
