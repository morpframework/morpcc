from ..app import App
from .model import BackRelationshipCollection, BackRelationshipModel

#
from .modelui import BackRelationshipCollectionUI, BackRelationshipModelUI
from .path import get_collection, get_model
from .schema import BackRelationshipSchema

#


@App.typeinfo(name="morpcc.backrelationship", schema=BackRelationshipSchema)
def get_typeinfo(request):
    return {
        "title": "BackRelationship",
        "description": "BackRelationship type",
        "schema": BackRelationshipSchema,
        "collection": BackRelationshipCollection,
        "collection_factory": get_collection,
        "model": BackRelationshipModel,
        "model_factory": get_model,
        #
        "collection_ui": BackRelationshipCollectionUI,
        "model_ui": BackRelationshipModelUI,
        "internal": True
        #
    }
