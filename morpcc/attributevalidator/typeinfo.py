from ..app import App
from .model import AttributeValidatorCollection
from .model import AttributeValidatorModel
from .schema import AttributeValidatorSchema
from .path import get_collection, get_model

#
from .modelui import AttributeValidatorCollectionUI
from .modelui import AttributeValidatorModelUI
from .path import get_collection_ui, get_model_ui

#


@App.typeinfo(name="morpcc.attributevalidator", schema=AttributeValidatorSchema)
def get_typeinfo(request):
    return {
        "title": "AttributeValidator",
        "description": "AttributeValidator type",
        "schema": AttributeValidatorSchema,
        "collection": AttributeValidatorCollection,
        "collection_factory": get_collection,
        "model": AttributeValidatorModel,
        "model_factory": get_model,
        #
        "collection_ui": AttributeValidatorCollectionUI,
        "collection_ui_factory": get_collection_ui,
        "model_ui": AttributeValidatorModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
