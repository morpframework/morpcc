from morpfw.crud import permission as crudperm
from ..app import App
from .model import ApplicationModel, ApplicationCollection
from .modelui import ApplicationModelUI, ApplicationCollectionUI


@App.permission_rule(model=ApplicationCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=ApplicationModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=ApplicationCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=ApplicationModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
