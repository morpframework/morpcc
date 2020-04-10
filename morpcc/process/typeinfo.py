from ..app import App
from .model import ProcessCollection
from .model import ProcessModel
from .schema import ProcessSchema
from .path import get_collection, get_model
# 
from .modelui import ProcessCollectionUI
from .modelui import ProcessModelUI
# 


@App.typeinfo(
    name='morpcc.process',
    schema=ProcessSchema)
def get_typeinfo(request):
    return {
        'title': 'Process',
        'description': 'Process type',
        'schema': ProcessSchema,
        'collection': ProcessCollection,
        'collection_factory': get_collection,
        'model': ProcessModel,
        'model_factory': get_model,
        # 
        'collection_ui': ProcessCollectionUI,
        'model_ui': ProcessModelUI,
        # 
    }
