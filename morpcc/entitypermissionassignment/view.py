from urllib.parse import quote as urlquote

from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm

from ..app import App
from ..entitycontent.modelui import EntityContentCollectionUI

#
from ..permission import ManagePermission
from .model import EntityPermissionAssignmentCollection, EntityPermissionAssignmentModel

#
from .modelui import (
    EntityPermissionAssignmentCollectionUI,
    EntityPermissionAssignmentModelUI,
)


@App.html(
    model=EntityContentCollectionUI,
    name="manage-permissions",
    template="master/permission/entity.pt",
    permission=ManagePermission,
)
def manage_permission(context, request):
    app = context.collection.application()
    entity = context.collection.entity()
    return {
        "page_title": "Manage Permissions",
        "application": app,
        "entity": entity,
        "table_filter": urlquote(
            "application_uuid=='%s' and entity_uuid=='%s'" % (app.uuid, entity.uuid)
        ),
    }
