from ..app import App
from .model import ReferenceDataPropertyCollection, ReferenceDataPropertyModel

#
from .modelui import ReferenceDataPropertyCollectionUI, ReferenceDataPropertyModelUI
from .path import get_collection, get_model
from .schema import ReferenceDataPropertySchema

#


@App.typeinfo(name="morpcc.referencedataproperty", schema=ReferenceDataPropertySchema)
def get_typeinfo(request):
    return {
        "title": "ReferenceDataProperty",
        "description": "ReferenceDataProperty type",
        "schema": ReferenceDataPropertySchema,
        "collection": ReferenceDataPropertyCollection,
        "collection_factory": get_collection,
        "model": ReferenceDataPropertyModel,
        "model_factory": get_model,
        #
        "collection_ui": ReferenceDataPropertyCollectionUI,
        "model_ui": ReferenceDataPropertyModelUI,
        #
        "internal": True,
    }
