from ..app import App
from .model import (
    DictionaryElementValidatorAssignmentCollection,
    DictionaryElementValidatorAssignmentModel,
)

#
from .modelui import (
    DictionaryElementValidatorAssignmentCollectionUI,
    DictionaryElementValidatorAssignmentModelUI,
)
from .path import get_collection, get_model
from .schema import DictionaryElementValidatorAssignmentSchema

#


@App.typeinfo(
    name="morpcc.dictionaryelementvalidatorassignment",
    schema=DictionaryElementValidatorAssignmentSchema,
)
def get_typeinfo(request):
    return {
        "title": "DictionaryElementValidatorAssignment",
        "description": "DictionaryElementValidatorAssignment type",
        "schema": DictionaryElementValidatorAssignmentSchema,
        "collection": DictionaryElementValidatorAssignmentCollection,
        "collection_factory": get_collection,
        "model": DictionaryElementValidatorAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": DictionaryElementValidatorAssignmentCollectionUI,
        "model_ui": DictionaryElementValidatorAssignmentModelUI,
        #
        "internal": True,
    }
