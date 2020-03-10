from ..app import App
from .model import BehaviorAssignmentCollection, BehaviorAssignmentModel

#
from .modelui import BehaviorAssignmentCollectionUI, BehaviorAssignmentModelUI
from .path import get_collection, get_model
from .schema import BehaviorAssignmentSchema

#


@App.typeinfo(name="morpcc.behaviorassignment", schema=BehaviorAssignmentSchema)
def get_typeinfo(request):
    return {
        "title": "BehaviorAssignment",
        "description": "BehaviorAssignment type",
        "schema": BehaviorAssignmentSchema,
        "collection": BehaviorAssignmentCollection,
        "collection_factory": get_collection,
        "model": BehaviorAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": BehaviorAssignmentCollectionUI,
        "model_ui": BehaviorAssignmentModelUI,
        "internal": True
        #
    }
