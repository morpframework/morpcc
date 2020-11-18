import morpfw
import morpfw.crud.signals as signals
import rulez
from morpcc.navigator import Navigator

from ..app import App
from ..entitycontent.model import (EntityContentCollection, EntityContentModel,
                                   content_collection_factory)
from .model import ApplicationModel


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_CREATED)
def index_on_create(app, request, context, signal):
    if request.environ.get("morpcc.noindexing", False):
        return
    app_uuid = context.collection.__application__.uuid
    entity = context.collection.entity()

    queue = request.get_collection("morpcc.entitycontentindexqueue")
    queue.create(
        {
            "application_uuid": app_uuid,
            "entity_uuid": entity.uuid,
            "record_uuid": context.uuid,
            "action": "index",
        }
    )


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_UPDATED)
def index_on_update(app, request, context, signal):
    if request.environ.get("morpcc.noindexing", False):
        return
    app_uuid = context.collection.__application__.uuid
    entity = context.collection.entity()
    queue = request.get_collection("morpcc.entitycontentindexqueue")
    queue.create(
        {
            "application_uuid": app_uuid,
            "entity_uuid": entity.uuid,
            "record_uuid": context.uuid,
            "action": "index",
        }
    )


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_TOBEDELETED)
def unindex_on_delete(app, request, context, signal):
    app_uuid = context.collection.__application__.uuid
    entity = context.collection.entity()
    queue = request.get_collection("morpcc.entitycontentindexqueue")
    queue.create(
        {
            "application_uuid": app_uuid,
            "entity_uuid": entity.uuid,
            "record_uuid": context.uuid,
            "action": "unindex",
        }
    )
