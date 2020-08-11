import rulez
from morpcc.crud.model import CollectionUI, ModelUI
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from morpfw.crud.model import Collection, Model

from ..app import App
from .model import PermissionAssignmentCollection, PermissionAssignmentModel

#
from .modelui import PermissionAssignmentCollectionUI, PermissionAssignmentModelUI


#
def _name(klass):
    if klass:
        return "%s:%s" % (klass.__module__, klass.__name__)


@App.json(
    model=CollectionUI,
    name="manage-permissions",
    #    template="master/permission/manage.pt",
)
def maange_permission(context, request):
    typeinfo = request.app.get_typeinfo_by_schema(context.collection.schema, request)

    model = _name(typeinfo["model"])
    collection = _name(typeinfo["collection"])
    model_ui = _name(typeinfo.get("model_ui", None))
    collection_ui = _name(typeinfo.get("collection_ui", None))

    assignmentcol = request.get_collection("morpcc.permissionassignment")
    assignments = []
    for m in [model, collection, model_ui, collection_ui]:
        if m is None:
            continue

        perms = assignmentcol.search(rulez.field["model"] == m)

        assignments.append(
            {
                "model": m,
                "permissions": [
                    {
                        "permission": p["permission"],
                        "groups": p["groups"],
                        "users": p["users"],
                    }
                    for p in perms
                ],
            }
        )
    return {
        "assignments": assignments,
        "model": model,
        "name": typeinfo["name"],
        "title": typeinfo["title"],
        "model_ui": model_ui,
        "collection": collection,
        "collection_ui": collection_ui,
    }
