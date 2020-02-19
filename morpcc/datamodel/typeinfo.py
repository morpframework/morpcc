from ..app import App
from .model import DataModelCollection
from .model import DataModelModel
from .schema import DataModelSchema
from .path import get_collection, get_model
# 
from .modelui import DataModelCollectionUI
from .modelui import DataModelModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.datamodel', schema=DataModelSchema)
def get_typeinfo(request):
    return {
        'title': 'DataModel',
        'description': 'DataModel type',
        'schema': DataModelSchema,
        'collection': DataModelCollection,
        'collection_factory': get_collection,
        'model': DataModelModel,
        'model_factory': get_model,
        # 
        'collection_ui': DataModelCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': DataModelModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
