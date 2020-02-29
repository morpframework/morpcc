from morpfw.crud import permission as crudperm
from ..app import App
from .model import EndpointModel, EndpointCollection
from .modelui import EndpointModelUI, EndpointCollectionUI


@App.permission_rule(model=EndpointCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=EndpointModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=EndpointCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=EndpointModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
