from ..app import App
from .model import EntityValidatorCollection, EntityValidatorModel

#
from .modelui import EntityValidatorCollectionUI, EntityValidatorModelUI
from .path import get_collection, get_model
from .schema import EntityValidatorSchema

#


@App.typeinfo(name="morpcc.entityvalidator", schema=EntityValidatorSchema)
def get_typeinfo(request):
    return {
        "title": "EntityValidator",
        "description": "EntityValidator type",
        "schema": EntityValidatorSchema,
        "collection": EntityValidatorCollection,
        "collection_factory": get_collection,
        "model": EntityValidatorModel,
        "model_factory": get_model,
        #
        "collection_ui": EntityValidatorCollectionUI,
        "model_ui": EntityValidatorModelUI,
        "internal": True
        #
    }
