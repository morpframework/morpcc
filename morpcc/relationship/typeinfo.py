from ..app import App
from .model import RelationshipCollection
from .model import RelationshipModel
from .schema import RelationshipSchema
from .path import get_collection, get_model
# 
from .modelui import RelationshipCollectionUI
from .modelui import RelationshipModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.relationship', schema=RelationshipSchema)
def get_typeinfo(request):
    return {
        'title': 'Relationship',
        'description': 'Relationship type',
        'schema': RelationshipSchema,
        'collection': RelationshipCollection,
        'collection_factory': get_collection,
        'model': RelationshipModel,
        'model_factory': get_model,
        # 
        'collection_ui': RelationshipCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': RelationshipModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
