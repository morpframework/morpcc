import rulez
from morpfw.crud import permission as crudperm
from morpfw.crud.model import Collection, Model
from morpfw.permission import All as MFWAll

from morpcc.authz import rule_from_assignment

from .app import App
from .authz.permission_rule import eval_permissions
from .crud.model import CollectionUI, ModelUI
from .root import Root
from .users.model import CurrentUserModelUI


@App.permission_rule(model=Root, permission=MFWAll)
def root_view_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


@App.permission_resolver()
def resolve_model_permission(request, model, permission, identity):
    opcol = request.get_collection("morpcc.objectpermissionassignment")
    # find object permission
    if isinstance(model, Model) or isinstance(model, ModelUI):
        found_perms = opcol.search(
            rulez.and_(
                rulez.field["object_uuid"] == model.uuid,
                rulez.field["enabled"] == True,
            )
        )

        res = eval_permissions(request, model, permission, found_perms, identity)
        if res is not None:
            return res
