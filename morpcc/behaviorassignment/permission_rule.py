from morpfw.crud import permission as crudperm
from ..app import App
from .model import BehaviorAssignmentModel, BehaviorAssignmentCollection
from .modelui import BehaviorAssignmentModelUI, BehaviorAssignmentCollectionUI


@App.permission_rule(model=BehaviorAssignmentCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=BehaviorAssignmentModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=BehaviorAssignmentCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=BehaviorAssignmentModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
