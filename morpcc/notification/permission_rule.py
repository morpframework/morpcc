from morpfw.crud import permission as crudperm
from ..app import App
from .model import NotificationModel, NotificationCollection
from .modelui import NotificationModelUI, NotificationCollectionUI


@App.permission_rule(model=NotificationCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=NotificationModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=NotificationCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=NotificationModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
