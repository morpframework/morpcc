from morpfw.crud import permission as crudperm
from ..app import App
from .model import EndpointHandlerModel, EndpointHandlerCollection
from .modelui import EndpointHandlerModelUI, EndpointHandlerCollectionUI


@App.permission_rule(model=EndpointHandlerCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=EndpointHandlerModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=EndpointHandlerCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=EndpointHandlerModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
