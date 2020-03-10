from ..app import App
from .model import ReferenceDataCollection, ReferenceDataModel

#
from .modelui import ReferenceDataCollectionUI, ReferenceDataModelUI
from .path import get_collection, get_model
from .schema import ReferenceDataSchema

#


@App.typeinfo(name="morpcc.referencedata", schema=ReferenceDataSchema)
def get_typeinfo(request):
    return {
        "title": "ReferenceData",
        "description": "ReferenceData type",
        "schema": ReferenceDataSchema,
        "collection": ReferenceDataCollection,
        "collection_factory": get_collection,
        "model": ReferenceDataModel,
        "model_factory": get_model,
        #
        "collection_ui": ReferenceDataCollectionUI,
        "model_ui": ReferenceDataModelUI,
        #
        "internal": True,
    }
