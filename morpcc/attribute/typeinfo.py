from ..app import App
from .model import AttributeCollection
from .model import AttributeModel
from .schema import AttributeSchema
from .path import get_collection, get_model
# 
from .modelui import AttributeCollectionUI
from .modelui import AttributeModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.attribute')
def get_typeinfo(request):
    return {
        'title': 'Attribute',
        'description': 'Attribute type',
        'schema': AttributeSchema,
        'collection': AttributeCollection,
        'collection_factory': get_collection,
        'model': AttributeModel,
        'model_factory': get_model,
        # 
        'collection_ui': AttributeCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': AttributeModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
