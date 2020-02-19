from ..app import App
from .model import IndexCollection
from .model import IndexModel
from .schema import IndexSchema
from .path import get_collection, get_model
# 
from .modelui import IndexCollectionUI
from .modelui import IndexModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(name='morpcc.index')
def get_typeinfo(request):
    return {
        'title': 'Index',
        'description': 'Index type',
        'schema': IndexSchema,
        'collection': IndexCollection,
        'collection_factory': get_collection,
        'model': IndexModel,
        'model_factory': get_model,
        # 
        'collection_ui': IndexCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': IndexModelUI,
        'model_ui_factory': get_model_ui,
        # 
    }
