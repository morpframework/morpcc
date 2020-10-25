from ..app import App
from .model import EntityPermissionAssignmentCollection
from .model import EntityPermissionAssignmentModel
from .schema import EntityPermissionAssignmentSchema
from .path import get_collection, get_model
# 
from .modelui import EntityPermissionAssignmentCollectionUI
from .modelui import EntityPermissionAssignmentModelUI
# 


@App.typeinfo(
    name='morpcc.entitypermissionassignment',
    schema=EntityPermissionAssignmentSchema)
def get_typeinfo(request):
    return {
        'title': 'EntityPermissionAssignment',
        'description': 'EntityPermissionAssignment type',
        'schema': EntityPermissionAssignmentSchema,
        'collection': EntityPermissionAssignmentCollection,
        'collection_factory': get_collection,
        'model': EntityPermissionAssignmentModel,
        'model_factory': get_model,
        # 
        'collection_ui': EntityPermissionAssignmentCollectionUI,
        'model_ui': EntityPermissionAssignmentModelUI,
        # 
    }
