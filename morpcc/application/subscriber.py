import morpfw
import morpfw.crud.signals as signals
import rulez
from morpcc.navigator import Navigator

from ..app import App
from ..entitycontent.model import (
    EntityContentCollection,
    EntityContentModel,
    content_collection_factory,
)
from .model import ApplicationModel

BATCH_SIZE = 1000


@App.periodic(name="morpcc.scheduler.index", seconds=600)
def periodic_indexing(request_options):
    with morpfw.request_factory(**request_options) as request:
        queue = request.get_collection("morpcc.entitycontentindexqueue")
        if queue.search(rulez.field["action"] == "index", limit=1):
            request.async_dispatch("morpcc.entitycontent.index")
        if queue.search(rulez.field["action"] == "unindex", limit=1):
            request.async_dispatch("morpcc.entitycontent.unindex")


@App.async_subscribe("morpcc.entitycontent.index")
def index(request_options):
    with morpfw.request_factory(**request_options) as request:
        queue = request.get_collection("morpcc.entitycontentindexqueue")
        items = queue.search(rulez.field["action"] == "index", limit=BATCH_SIZE)
        for i in items:
            app_uuid = i["application_uuid"]
            entity_uuid = i["entity_uuid"]
            uuid = i["record_uuid"]
            appcol = request.get_collection("morpcc.application")
            entitycol = request.get_collection("morpcc.entity")
            app = appcol.get(app_uuid)
            entity = entitycol.get(entity_uuid)
            content_col = content_collection_factory(entity, app)
            context = content_col.get(uuid)
            app.index_sync(context)

        for i in items:
            i.delete()


@App.async_subscribe("morpcc.entitycontent.unindex")
def index(request_options):
    with morpfw.request_factory(**request_options) as request:
        queue = request.get_collection("morpcc.entitycontentindexqueue")
        items = queue.search(rulez.field["action"] == "unindex", limit=BATCH_SIZE)

        for i in items:
            app_uuid = i["application_uuid"]
            entity_uuid = i["entity_uuid"]
            uuid = i["record_uuid"]
            appcol = request.get_collection("morpcc.application")
            entitycol = request.get_collection("morpcc.entity")
            app = appcol.get(app_uuid)
            entity = entitycol.get(entity_uuid)
            content_col = content_collection_factory(entity, app)
            context = content_col.get(uuid)
            app.unindex(context)

        for i in items:
            i.delete()


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
