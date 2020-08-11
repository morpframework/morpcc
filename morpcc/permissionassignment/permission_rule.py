from morpfw.crud import permission as crudperm
from ..app import App
from .model import PermissionAssignmentModel, PermissionAssignmentCollection
from .modelui import PermissionAssignmentModelUI, PermissionAssignmentCollectionUI


@App.permission_rule(model=PermissionAssignmentCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=PermissionAssignmentModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=PermissionAssignmentCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=PermissionAssignmentModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
