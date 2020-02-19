from morpfw.crud import permission as crudperm
from ..app import App
from .model import AttributeConstraintModel, AttributeConstraintCollection
from .modelui import AttributeConstraintModelUI, AttributeConstraintCollectionUI


@App.permission_rule(model=AttributeConstraintCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=AttributeConstraintModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=AttributeConstraintCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=AttributeConstraintModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

#

