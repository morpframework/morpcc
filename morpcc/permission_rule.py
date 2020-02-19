from .app import App
from .root import Root
from .users.model import CurrentUserModelUI
from morpfw.crud import permission as crudperm
from . import permission


@App.permission_rule(model=Root, permission=permission.ViewHome)
def root_view_permission(identity, model, permission):
    return True


@App.permission_rule(model=Root, permission=permission.ManageSite)
def root_manage_site(identity, model, permission):
    return True


@App.permission_rule(model=Root, permission=permission.SiteSearch)
def root_site_search(identity, model, permission):
    return True
