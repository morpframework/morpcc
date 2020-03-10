from ..app import App
from .model import AttributeValidatorCollection, AttributeValidatorModel

#
from .modelui import AttributeValidatorCollectionUI, AttributeValidatorModelUI
from .path import get_collection, get_model
from .schema import AttributeValidatorSchema

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
        "model_ui": AttributeValidatorModelUI,
        "internal": True
        #
    }
