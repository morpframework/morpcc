from ..app import App
from .model import (
    AttributeValidatorAssignmentCollection,
    AttributeValidatorAssignmentModel,
)

#
from .modelui import (
    AttributeValidatorAssignmentCollectionUI,
    AttributeValidatorAssignmentModelUI,
)
from .path import get_collection, get_model
from .schema import AttributeValidatorAssignmentSchema

#


@App.typeinfo(
    name="morpcc.attributevalidatorassignment",
    schema=AttributeValidatorAssignmentSchema,
)
def get_typeinfo(request):
    return {
        "title": "AttributeValidatorAssignment",
        "description": "AttributeValidatorAssignment type",
        "schema": AttributeValidatorAssignmentSchema,
        "collection": AttributeValidatorAssignmentCollection,
        "collection_factory": get_collection,
        "model": AttributeValidatorAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": AttributeValidatorAssignmentCollectionUI,
        "model_ui": AttributeValidatorAssignmentModelUI,
        "internal": True
        #
    }
