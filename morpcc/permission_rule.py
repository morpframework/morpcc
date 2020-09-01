from morpcc.authz import rule_from_assignment
from morpfw.crud import permission as crudperm
from morpfw.permission import All as MFWAll

from . import permission
from .app import App
from .root import Root
from .users.model import CurrentUserModelUI


@App.permission_rule(model=Root, permission=MFWAll)
def root_view_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)
