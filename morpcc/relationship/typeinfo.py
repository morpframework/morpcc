from ..app import App
from .model import RelationshipCollection, RelationshipModel

#
from .modelui import RelationshipCollectionUI, RelationshipModelUI
from .path import get_collection, get_model
from .schema import RelationshipSchema

#


@App.typeinfo(name="morpcc.relationship", schema=RelationshipSchema)
def get_typeinfo(request):
    return {
        "title": "Relationship",
        "description": "Relationship type",
        "schema": RelationshipSchema,
        "collection": RelationshipCollection,
        "collection_factory": get_collection,
        "model": RelationshipModel,
        "model_factory": get_model,
        #
        "collection_ui": RelationshipCollectionUI,
        "model_ui": RelationshipModelUI,
        "internal": True
        #
    }
