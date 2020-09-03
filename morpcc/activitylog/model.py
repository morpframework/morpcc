import morpfw
from morpcc.authn import Identity

from ..entitycontent.model import EntityContentModel
from .modelui import ActivityLogCollectionUI, ActivityLogModelUI
from .schema import ActivityLogSchema

#


class ActivityLogModel(morpfw.Model):
    schema = ActivityLogSchema

    #
    def ui(self):
        return ActivityLogModelUI(self.request, self, self.collection.ui())


#


class ActivityLogCollection(morpfw.Collection):
    schema = ActivityLogSchema

    #
    def ui(self):
        return ActivityLogCollectionUI(self.request, self)

    #

    def log(self, context, activity):
        if isinstance(context, ActivityLogModel):
            return
        request = self.request
        if isinstance(request.identity, Identity):
            userid = request.identity.userid
        else:
            userid = None
        if isinstance(context, EntityContentModel):
            app = context.application()
            entity = context.entity()
            type_name = "morpcc.application.%s.%s.%s" % (
                app.uuid,
                app["name"],
                entity["name"],
            )
        else:
            type_name = request.app.get_typeinfo_by_schema(
                context.schema, request=request
            )["name"]
        view_name = getattr(request, "view_name", None)
        self.create(
            {
                "userid": userid,
                "resource_uuid": context.uuid,
                "resource_type": type_name,
                "view_name": view_name,
                "activity": activity,
                "source_ip": request.client_addr,
            }
        )