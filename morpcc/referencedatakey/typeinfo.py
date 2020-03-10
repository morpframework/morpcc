from ..app import App
from .model import ReferenceDataKeyCollection, ReferenceDataKeyModel

#
from .modelui import ReferenceDataKeyCollectionUI, ReferenceDataKeyModelUI
from .path import get_collection, get_model
from .schema import ReferenceDataKeySchema

#


@App.typeinfo(name="morpcc.referencedatakey", schema=ReferenceDataKeySchema)
def get_typeinfo(request):
    return {
        "title": "ReferenceDataKey",
        "description": "ReferenceDataKey type",
        "schema": ReferenceDataKeySchema,
        "collection": ReferenceDataKeyCollection,
        "collection_factory": get_collection,
        "model": ReferenceDataKeyModel,
        "model_factory": get_model,
        #
        "collection_ui": ReferenceDataKeyCollectionUI,
        "model_ui": ReferenceDataKeyModelUI,
        "internal": True
        #
    }
