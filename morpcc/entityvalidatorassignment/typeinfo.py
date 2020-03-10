from ..app import App
from .model import EntityValidatorAssignmentCollection
from .model import EntityValidatorAssignmentModel
from .schema import EntityValidatorAssignmentSchema
from .path import get_collection, get_model
# 
from .modelui import EntityValidatorAssignmentCollectionUI
from .modelui import EntityValidatorAssignmentModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(
    name='morpcc.entityvalidatorassignment',
    schema=EntityValidatorAssignmentSchema)
def get_typeinfo(request):
    return {
        'title': 'EntityValidatorAssignment',
        'description': 'EntityValidatorAssignment type',
        'schema': EntityValidatorAssignmentSchema,
        'collection': EntityValidatorAssignmentCollection,
        'collection_factory': get_collection,
        'model': EntityValidatorAssignmentModel,
        'model_factory': get_model,
        # 
        'collection_ui': EntityValidatorAssignmentCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': EntityValidatorAssignmentModelUI,
        'model_ui_factory': get_model_ui,
        # 
    }
