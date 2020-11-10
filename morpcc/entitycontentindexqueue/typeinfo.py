from ..app import App
from .model import EntityContentIndexQueueCollection, EntityContentIndexQueueModel

#
from .modelui import EntityContentIndexQueueCollectionUI, EntityContentIndexQueueModelUI
from .path import get_collection, get_model
from .schema import EntityContentIndexQueueSchema

#


@App.typeinfo(
    name="morpcc.entitycontentindexqueue", schema=EntityContentIndexQueueSchema
)
def get_typeinfo(request):
    return {
        "title": "EntityContentIndexQueue",
        "description": "EntityContentIndexQueue type",
        "schema": EntityContentIndexQueueSchema,
        "collection": EntityContentIndexQueueCollection,
        "collection_factory": get_collection,
        "model": EntityContentIndexQueueModel,
        "model_factory": get_model,
        #
        "collection_ui": EntityContentIndexQueueCollectionUI,
        "model_ui": EntityContentIndexQueueModelUI,
        "internal": True
        #
    }
