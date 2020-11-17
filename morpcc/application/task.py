import morpfw
import rulez

from ..app import App


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
