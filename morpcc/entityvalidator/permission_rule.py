from morpfw.crud import permission as crudperm
from ..app import App
from .model import EntityValidatorModel, EntityValidatorCollection
from .modelui import EntityValidatorModelUI, EntityValidatorCollectionUI


@App.permission_rule(model=EntityValidatorCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=EntityValidatorModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=EntityValidatorCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=EntityValidatorModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

#

