from ..app import App
from .model import BackRelationshipCollection
from .model import BackRelationshipModel
from .schema import BackRelationshipSchema
from .path import get_collection, get_model
# 
from .modelui import BackRelationshipCollectionUI
from .modelui import BackRelationshipModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.backrelationship', schema=BackRelationshipSchema)
def get_typeinfo(request):
    return {
        'title': 'BackRelationship',
        'description': 'BackRelationship type',
        'schema': BackRelationshipSchema,
        'collection': BackRelationshipCollection,
        'collection_factory': get_collection,
        'model': BackRelationshipModel,
        'model_factory': get_model,
        # 
        'collection_ui': BackRelationshipCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': BackRelationshipModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
