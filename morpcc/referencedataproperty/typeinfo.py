from ..app import App
from .model import ReferenceDataPropertyCollection
from .model import ReferenceDataPropertyModel
from .schema import ReferenceDataPropertySchema
from .path import get_collection, get_model

#
from .modelui import ReferenceDataPropertyCollectionUI
from .modelui import ReferenceDataPropertyModelUI
from .path import get_collection_ui, get_model_ui

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
        "collection_ui_factory": get_collection_ui,
        "model_ui": ReferenceDataPropertyModelUI,
        "model_ui_factory": get_model_ui,
        #
        "internal": True,
    }

