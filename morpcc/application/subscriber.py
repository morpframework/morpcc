import morpfw
import morpfw.crud.signals as signals
from morpcc.navigator import Navigator

from ..app import App
from ..entitycontent.model import (
    EntityContentCollection,
    EntityContentModel,
    content_collection_factory,
)
from .model import ApplicationModel


@App.async_subscribe("morpcc.entitycontent.index")
def index(request_options, app_uuid, entity_uuid, uuid):
    with morpfw.request_factory(**request_options) as request:
        appcol = request.get_collection("morpcc.application")
        entitycol = request.get_collection("morpcc.entity")
        app = appcol.get(app_uuid)
        entity = entitycol.get(entity_uuid)
        content_col = content_collection_factory(entity, app)
        context = content_col.get(uuid)
        app.index_sync(context)


@App.async_subscribe("morpcc.entitycontent.unindex")
def index(request_options, app_uuid, entity_uuid, uuid):
    with morpfw.request_factory(**request_options) as request:
        appcol = request.get_collection("morpcc.application")
        entitycol = request.get_collection("morpcc.entity")
        app = appcol.get(app_uuid)
        entity = entitycol.get(entity_uuid)
        content_col = content_collection_factory(entity, app)
        context = content_col.get(uuid)
        app.unindex(context)


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_CREATED)
def index_on_create(app, request, context, signal):
    if request.environ.get("morpcc.noindexing", False):
        return
    app_uuid = context.collection.__application__.uuid
    entity = context.collection.entity()
    request.async_dispatch(
        "morpcc.entitycontent.index",
        app_uuid=app_uuid,
        entity_uuid=entity.uuid,
        uuid=context.uuid,
    )


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_UPDATED)
def index_on_update(app, request, context, signal):
    if request.environ.get("morpcc.noindexing", False):
        return
    app_uuid = context.collection.__application__.uuid
    entity = context.collection.entity()
    request.async_dispatch(
        "morpcc.entitycontent.index",
        app_uuid=app_uuid,
        entity_uuid=entity.uuid,
        uuid=context.uuid,
    )


@App.subscribe(model=EntityContentModel, signal=signals.OBJECT_TOBEDELETED)
def unindex_on_delete(app, request, context, signal):
    app_uuid = context.collection.__application__.uuid
    entity = context.collection.entity()
    request.async_dispatch(
        "morpcc.entitycontent.unindex",
        app_uuid=app_uuid,
        entity_uuid=entity.uuid,
        uuid=context.uuid,
    )


@App.subscribe(model=ApplicationModel, signal=signals.OBJECT_TOBEDELETED)
def delete_schema(app, request, context, signal):
    app_uuid = context.uuid
    context: ApplicationModel = context
    context.drop_all()
