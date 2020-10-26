from ..app import App
from .model import EntityPermissionAssignmentCollection, EntityPermissionAssignmentModel

#
from .modelui import (
    EntityPermissionAssignmentCollectionUI,
    EntityPermissionAssignmentModelUI,
)
from .path import get_collection, get_model
from .schema import EntityPermissionAssignmentSchema

#


@App.typeinfo(
    name="morpcc.entitypermissionassignment", schema=EntityPermissionAssignmentSchema
)
def get_typeinfo(request):
    return {
        "title": "EntityPermissionAssignment",
        "description": "EntityPermissionAssignment type",
        "schema": EntityPermissionAssignmentSchema,
        "collection": EntityPermissionAssignmentCollection,
        "collection_factory": get_collection,
        "model": EntityPermissionAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": EntityPermissionAssignmentCollectionUI,
        "model_ui": EntityPermissionAssignmentModelUI,
        "internal": True
        #
    }
