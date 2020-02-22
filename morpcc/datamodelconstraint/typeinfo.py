from ..app import App
from .model import EntityConstraintCollection
from .model import EntityConstraintModel
from .schema import EntityConstraintSchema
from .path import get_collection, get_model
# 
from .modelui import EntityConstraintCollectionUI
from .modelui import EntityConstraintModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.entityconstraint', schema=EntityConstraintSchema)
def get_typeinfo(request):
    return {
        'title': 'EntityConstraint',
        'description': 'EntityConstraint type',
        'schema': EntityConstraintSchema,
        'collection': EntityConstraintCollection,
        'collection_factory': get_collection,
        'model': EntityConstraintModel,
        'model_factory': get_model,
        # 
        'collection_ui': EntityConstraintCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': EntityConstraintModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
