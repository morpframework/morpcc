from ..app import App
from .model import EndpointCollection
from .model import EndpointModel
from .schema import EndpointSchema
from .path import get_collection, get_model
# 
from .modelui import EndpointCollectionUI
from .modelui import EndpointModelUI
from .path import get_collection_ui, get_model_ui
# 


@App.typeinfo(
    name='morpcc.endpoint',
    schema=EndpointSchema)
def get_typeinfo(request):
    return {
        'title': 'Endpoint',
        'description': 'Endpoint type',
        'schema': EndpointSchema,
        'collection': EndpointCollection,
        'collection_factory': get_collection,
        'model': EndpointModel,
        'model_factory': get_model,
        # 
        'collection_ui': EndpointCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': EndpointModelUI,
        'model_ui_factory': get_model_ui,
        # 
    }
