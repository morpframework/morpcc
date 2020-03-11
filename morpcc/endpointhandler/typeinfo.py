from ..app import App
from .model import EndpointHandlerCollection
from .model import EndpointHandlerModel
from .schema import EndpointHandlerSchema
from .path import get_collection, get_model
# 
from .modelui import EndpointHandlerCollectionUI
from .modelui import EndpointHandlerModelUI
# 


@App.typeinfo(
    name='morpcc.endpointhandler',
    schema=EndpointHandlerSchema)
def get_typeinfo(request):
    return {
        'title': 'EndpointHandler',
        'description': 'EndpointHandler type',
        'schema': EndpointHandlerSchema,
        'collection': EndpointHandlerCollection,
        'collection_factory': get_collection,
        'model': EndpointHandlerModel,
        'model_factory': get_model,
        # 
        'collection_ui': EndpointHandlerCollectionUI,
        'model_ui': EndpointHandlerModelUI,
        'internal': True
        # 
    }
