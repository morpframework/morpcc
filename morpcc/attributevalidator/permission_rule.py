from morpfw.crud import permission as crudperm
from ..app import App
from .model import AttributeValidatorModel, AttributeValidatorCollection
from .modelui import AttributeValidatorModelUI, AttributeValidatorCollectionUI


@App.permission_rule(model=AttributeValidatorCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=AttributeValidatorModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=AttributeValidatorCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=AttributeValidatorModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True


#

