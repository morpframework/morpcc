from ..app import App
from .model import ReferenceDataKeyCollection
from .model import ReferenceDataKeyModel
from .schema import ReferenceDataKeySchema
from .path import get_collection, get_model
# 
from .modelui import ReferenceDataKeyCollectionUI
from .modelui import ReferenceDataKeyModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.referencedatakey')
def get_typeinfo(request):
    return {
        'title': 'ReferenceDataKey',
        'description': 'ReferenceDataKey type',
        'schema': ReferenceDataKeySchema,
        'collection': ReferenceDataKeyCollection,
        'collection_factory': get_collection,
        'model': ReferenceDataKeyModel,
        'model_factory': get_model,
        # 
        'collection_ui': ReferenceDataKeyCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': ReferenceDataKeyModelUI,
        'model_ui_factory': get_model_ui,
        # 
    }
