from ..app import App
from .model import ReferenceDataCollection
from .model import ReferenceDataModel
from .schema import ReferenceDataSchema
from .path import get_collection, get_model
#
from .modelui import ReferenceDataCollectionUI
from .modelui import ReferenceDataModelUI
from .path import get_collection_ui, get_model_ui
#


@App.typeinfo(name='morpcc.referencedata')
def get_typeinfo(request):
    return {
        'title': 'ReferenceData',
        'description': 'ReferenceData type',
        'schema': ReferenceDataSchema,
        'collection': ReferenceDataCollection,
        'collection_factory': get_collection,
        'model': ReferenceDataModel,
        'model_factory': get_model,
        #
        'collection_ui': ReferenceDataCollectionUI,
        'collection_ui_factory': get_collection_ui,
        'model_ui': ReferenceDataModelUI,
        'model_ui_factory': get_model_ui,
        #
        'internal': True,
    }
