from ..app import App
from .model import AttributeValidatorAssignmentCollection
from .model import AttributeValidatorAssignmentModel
from .schema import AttributeValidatorAssignmentSchema
from .path import get_collection, get_model
# 
from .modelui import AttributeValidatorAssignmentCollectionUI
from .modelui import AttributeValidatorAssignmentModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(
    name='morpcc.attributevalidatorassignment',
    schema=AttributeValidatorAssignmentSchema)
def get_typeinfo(request):
    return {
        'title': 'AttributeValidatorAssignment',
        'description': 'AttributeValidatorAssignment type',
        'schema': AttributeValidatorAssignmentSchema,
        'collection': AttributeValidatorAssignmentCollection,
        'collection_factory': get_collection,
        'model': AttributeValidatorAssignmentModel,
        'model_factory': get_model,
        # 
        'collection_ui': AttributeValidatorAssignmentCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': AttributeValidatorAssignmentModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
