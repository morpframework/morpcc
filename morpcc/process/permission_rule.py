from morpfw.crud import permission as crudperm
from ..app import App
from .model import ProcessModel, ProcessCollection
from .modelui import ProcessModelUI, ProcessCollectionUI


@App.permission_rule(model=ProcessCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=ProcessModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=ProcessCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=ProcessModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
