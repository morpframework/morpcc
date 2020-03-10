from ..app import App
from .model import AttributeCollection, AttributeModel

#
from .modelui import AttributeCollectionUI, AttributeModelUI
from .path import get_collection, get_model
from .schema import AttributeSchema

#


@App.typeinfo(name="morpcc.attribute", schema=AttributeSchema)
def get_typeinfo(request):
    return {
        "title": "Attribute",
        "description": "Attribute type",
        "schema": AttributeSchema,
        "collection": AttributeCollection,
        "collection_factory": get_collection,
        "model": AttributeModel,
        "model_factory": get_model,
        #
        "collection_ui": AttributeCollectionUI,
        "model_ui": AttributeModelUI,
        "internal": True
        #
    }
