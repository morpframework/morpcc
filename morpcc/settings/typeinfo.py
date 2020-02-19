from ..app import App
from .model import SettingCollection
from .model import SettingModel
from .schema import SettingSchema
from .path import get_collection, get_model
# 
from .modelui import SettingCollectionUI
from .modelui import SettingModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.setting')
def get_typeinfo(request):
    return {
        'title': 'Setting',
        'description': 'Setting',
        'schema': SettingSchema,
        'collection': SettingCollection,
        'collection_factory': get_collection,
        'model': SettingModel,
        'model_factory': get_model,
        # 
        'collection_ui': SettingCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': SettingModelUI,
        'model_ui_factory': get_model_ui,
        'internal': True
        # 
    }
