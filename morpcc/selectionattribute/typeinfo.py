from ..app import App
from .model import SelectionAttributeCollection, SelectionAttributeModel

#
from .modelui import SelectionAttributeCollectionUI, SelectionAttributeModelUI
from .path import get_collection, get_collection_ui, get_model, get_model_ui
from .schema import SelectionAttributeSchema

#


@App.typeinfo(name="morpcc.selectionattribute", schema=SelectionAttributeSchema)
def get_typeinfo(request):
    return {
        "title": "SelectionAttribute",
        "description": "SelectionAttribute type",
        "schema": SelectionAttributeSchema,
        "collection": SelectionAttributeCollection,
        "collection_factory": get_collection,
        "model": SelectionAttributeModel,
        "model_factory": get_model,
        #
        "collection_ui": SelectionAttributeCollectionUI,
        "collection_ui_factory": get_collection_ui,
        "model_ui": SelectionAttributeModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
