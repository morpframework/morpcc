from morpfw.crud import permission as crudperm
from ..app import App
from .model import AttributeValidatorAssignmentModel, AttributeValidatorAssignmentCollection
from .modelui import AttributeValidatorAssignmentModelUI, AttributeValidatorAssignmentCollectionUI


@App.permission_rule(model=AttributeValidatorAssignmentCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=AttributeValidatorAssignmentModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=AttributeValidatorAssignmentCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=AttributeValidatorAssignmentModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
