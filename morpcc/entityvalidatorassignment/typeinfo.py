from ..app import App
from .model import EntityValidatorAssignmentCollection, EntityValidatorAssignmentModel

#
from .modelui import (
    EntityValidatorAssignmentCollectionUI,
    EntityValidatorAssignmentModelUI,
)
from .path import get_collection, get_model
from .schema import EntityValidatorAssignmentSchema

#


@App.typeinfo(
    name="morpcc.entityvalidatorassignment", schema=EntityValidatorAssignmentSchema
)
def get_typeinfo(request):
    return {
        "title": "EntityValidatorAssignment",
        "description": "EntityValidatorAssignment type",
        "schema": EntityValidatorAssignmentSchema,
        "collection": EntityValidatorAssignmentCollection,
        "collection_factory": get_collection,
        "model": EntityValidatorAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": EntityValidatorAssignmentCollectionUI,
        "model_ui": EntityValidatorAssignmentModelUI,
        "internal": True
        #
    }
