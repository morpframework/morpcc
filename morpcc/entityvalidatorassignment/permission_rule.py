from morpfw.crud import permission as crudperm
from ..app import App
from .model import EntityValidatorAssignmentModel, EntityValidatorAssignmentCollection
from .modelui import EntityValidatorAssignmentModelUI, EntityValidatorAssignmentCollectionUI


@App.permission_rule(model=EntityValidatorAssignmentCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=EntityValidatorAssignmentModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=EntityValidatorAssignmentCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=EntityValidatorAssignmentModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
