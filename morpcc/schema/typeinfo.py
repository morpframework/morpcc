from ..app import App
from .model import SchemaCollection, SchemaModel

#
from .modelui import SchemaCollectionUI, SchemaModelUI
from .path import get_collection, get_collection_ui, get_model, get_model_ui
from .schema import SchemaSchema

#


@App.typeinfo(name="morpcc.schema", schema=SchemaSchema)
def get_typeinfo(request):
    return {
        "title": "Schema",
        "description": "Schema type",
        "schema": SchemaSchema,
        "collection": SchemaCollection,
        "collection_factory": get_collection,
        "model": SchemaModel,
        "model_factory": get_model,
        #
        "collection_ui": SchemaCollectionUI,
        "collection_ui_factory": get_collection_ui,
        "model_ui": SchemaModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
