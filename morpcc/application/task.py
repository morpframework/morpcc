import morpfw
import rulez

from ..app import App
from ..entitycontent.model import (EntityContentCollection, EntityContentModel,
                                   content_collection_factory)
from .adapters import ApplicationDatabaseSyncAdapter

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
            if not app:
                continue
            content_col = content_collection_factory(entity, app)
            context = content_col.get(uuid)
            if context:
                app.index_sync(context)

        for i in items:
            i.delete()


@App.async_subscribe("morpcc.entitycontent.unindex")
def unindex(request_options):
    with morpfw.request_factory(**request_options) as request:
        queue = request.get_collection("morpcc.entitycontentindexqueue")
        items = queue.search(rulez.field["action"] == "unindex", limit=BATCH_SIZE)
        idxcol = request.get_collection("morpcc.index").content_collection()
        for i in items:
            app_uuid = i["application_uuid"]
            entity_uuid = i["entity_uuid"]
            uuid = i["record_uuid"]
            idxcol.unindex_raw(
                rulez.and_(
                    rulez.field("application_uuid") == app_uuid,
                    rulez.field("entity_uuid") == entity_uuid,
                    rulez.field("entity_content_uuid") == uuid,
                )
            )

        for i in items:
            i.delete()


@App.async_subscribe("morpcc.delete_application")
def delete_application(request_options):
    to_delete = []
    with morpfw.request_factory(**request_options) as request:
        app_col = request.get_collection("morpcc.application")
        apps = app_col.search(rulez.field("state") == "pending_delete")
        for app in apps:
            to_delete.append(app.uuid)
            sm = app.statemachine()
            sm.process_delete()

    with morpfw.request_factory(**request_options) as request:
        app_col = request.get_collection("morpcc.application")
        for uuid in to_delete:
            app = app_col.get(uuid)
            print("Deleting %s" % app["name"])
            for ec in app.entity_collections().values():
                ec.drop_all()
            app.storage.delete(uuid, app)


@App.async_subscribe("morpcc.upgrade_application")
def upgrade_application(request_options, app_name):
    with morpfw.request_factory(**request_options) as request:
        app_col = request.get_collection("morpcc.application")
        app = app_col.get_by_name(app_name)
        dbsync = ApplicationDatabaseSyncAdapter(app, request)
        if dbsync.need_update:
            dbsync.update()
        sm = app.statemachine()
        sm.upgrade_complete()
