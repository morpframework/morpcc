from ..app import App
from .model import EntityValidatorCollection
from .model import EntityValidatorModel
from .schema import EntityValidatorSchema
from .path import get_collection, get_model

#
from .modelui import EntityValidatorCollectionUI
from .modelui import EntityValidatorModelUI
from .path import get_collection_ui, get_model_ui

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
        "collection_ui_factory": get_collection_ui,
        "model_ui": EntityValidatorModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
