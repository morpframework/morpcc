from morpfw.crud import permission as crudperm

from ..app import App
from ..entitycontent.model import EntityContentCollection, EntityContentModel
from .model import EntityCollection, EntityModel
from .modelui import EntityCollectionUI, EntityModelUI


@App.permission_rule(model=EntityCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=EntityModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


@App.permission_rule(model=EntityContentCollection, permission=crudperm.All)
def allow_content_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=EntityContentModel, permission=crudperm.All)
def allow_content_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=EntityCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=EntityModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True


#
