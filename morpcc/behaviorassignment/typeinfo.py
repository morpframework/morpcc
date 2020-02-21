from ..app import App
from .model import BehaviorAssignmentCollection, BehaviorAssignmentModel

#
from .modelui import BehaviorAssignmentCollectionUI, BehaviorAssignmentModelUI
from .path import get_collection, get_collection_ui, get_model, get_model_ui
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
        "collection_ui_factory": get_collection_ui,
        "model_ui": BehaviorAssignmentModelUI,
        "model_ui_factory": get_model_ui,
        "internal": True
        #
    }
