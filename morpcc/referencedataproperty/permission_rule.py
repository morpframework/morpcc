from morpfw.crud import permission as crudperm
from ..app import App
from .model import ReferenceDataPropertyModel, ReferenceDataPropertyCollection
from .modelui import ReferenceDataPropertyModelUI, ReferenceDataPropertyCollectionUI


@App.permission_rule(model=ReferenceDataPropertyCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=ReferenceDataPropertyModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=ReferenceDataPropertyCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=ReferenceDataPropertyModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

#

