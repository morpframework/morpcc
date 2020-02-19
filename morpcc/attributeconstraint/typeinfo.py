from ..app import App
from .model import AttributeConstraintCollection
from .model import AttributeConstraintModel
from .schema import AttributeConstraintSchema
from .path import get_collection, get_model

#
from .modelui import AttributeConstraintCollectionUI
from .modelui import AttributeConstraintModelUI
from .path import get_collection_ui, get_model_ui

#


@App.typeinfo(name="morpcc.attributeconstraint", schema=AttributeConstraintSchema)
def get_typeinfo(request):
    return {
        "title": "AttributeConstraint",
        "description": "AttributeConstraint type",
        "schema": AttributeConstraintSchema,
        "collection": AttributeConstraintCollection,
        "collection_factory": get_collection,
        "model": AttributeConstraintModel,
        "model_factory": get_model,
        #
        "collection_ui": AttributeConstraintCollectionUI,
        "collection_ui_factory": get_collection_ui,
        "model_ui": AttributeConstraintModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
