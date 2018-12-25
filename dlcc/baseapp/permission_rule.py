from .app import App
from .root import Root
from morpfw.crud.permission import View


@App.permission_rule(model=Root, permission=View)
def root_view_permission(identity, model, permission):
    return True
