from ..app import App
from .model import DictionaryEntityCollection
from .model import DictionaryEntityModel
from .schema import DictionaryEntitySchema
from .path import get_collection, get_model
# 
from .modelui import DictionaryEntityCollectionUI
from .modelui import DictionaryEntityModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(
    name='morpcc.dictionaryentity',
    schema=DictionaryEntitySchema)
def get_typeinfo(request):
    return {
        'title': 'DictionaryEntity',
        'description': 'DictionaryEntity type',
        'schema': DictionaryEntitySchema,
        'collection': DictionaryEntityCollection,
        'collection_factory': get_collection,
        'model': DictionaryEntityModel,
        'model_factory': get_model,
        # 
        'collection_ui': DictionaryEntityCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': DictionaryEntityModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
