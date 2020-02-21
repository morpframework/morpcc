from morpfw.crud import permission as crudperm
from ..app import App
from .model import ApplicationBehaviorAssignmentModel, ApplicationBehaviorAssignmentCollection
from .modelui import ApplicationBehaviorAssignmentModelUI, ApplicationBehaviorAssignmentCollectionUI


@App.permission_rule(model=ApplicationBehaviorAssignmentCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=ApplicationBehaviorAssignmentModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=ApplicationBehaviorAssignmentCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=ApplicationBehaviorAssignmentModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
