from ..app import App
from .model import DataModelConstraintCollection
from .model import DataModelConstraintModel
from .schema import DataModelConstraintSchema
from .path import get_collection, get_model
# 
from .modelui import DataModelConstraintCollectionUI
from .modelui import DataModelConstraintModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.datamodelconstraint', schema=DataModelConstraintSchema)
def get_typeinfo(request):
    return {
        'title': 'DataModelConstraint',
        'description': 'DataModelConstraint type',
        'schema': DataModelConstraintSchema,
        'collection': DataModelConstraintCollection,
        'collection_factory': get_collection,
        'model': DataModelConstraintModel,
        'model_factory': get_model,
        # 
        'collection_ui': DataModelConstraintCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': DataModelConstraintModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
