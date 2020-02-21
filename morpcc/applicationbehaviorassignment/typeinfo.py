from ..app import App
from .model import ApplicationBehaviorAssignmentCollection
from .model import ApplicationBehaviorAssignmentModel
from .schema import ApplicationBehaviorAssignmentSchema
from .path import get_collection, get_model
# 
from .modelui import ApplicationBehaviorAssignmentCollectionUI
from .modelui import ApplicationBehaviorAssignmentModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.applicationbehaviorassignment',
            schema=ApplicationBehaviorAssignmentSchema)
def get_typeinfo(request):
    return {
        'title': 'ApplicationBehaviorAssignment',
        'description': 'ApplicationBehaviorAssignment type',
        'schema': ApplicationBehaviorAssignmentSchema,
        'collection': ApplicationBehaviorAssignmentCollection,
        'collection_factory': get_collection,
        'model': ApplicationBehaviorAssignmentModel,
        'model_factory': get_model,
        # 
        'collection_ui': ApplicationBehaviorAssignmentCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': ApplicationBehaviorAssignmentModelUI,
        'model_ui_factory': get_model_ui,
        # 
    }
