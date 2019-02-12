from ..app import App
from .model import PageCollection, PageModel
from .modelui import PageCollectionUI, PageModelUI
from .schema import PageSchema
from .path import get_collection, get_model
from .path import get_collection_ui, get_model_ui


@App.typeinfo(name='democms.page')
def get_typeinfo(request):
    return {
        'title': 'Page',
        'description': 'A simple page content type',
        'collection': PageCollection,
        'collection_factory': get_collection,
        'collection_ui': PageCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model': PageModel,
        'model_factory': get_model,
        'model_ui': PageModelUI,
        'model_ui_factory': PageModelUI,
        'schema': PageSchema
    }
