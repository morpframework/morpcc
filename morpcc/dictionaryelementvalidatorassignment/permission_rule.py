from morpfw.crud import permission as crudperm
from ..app import App
from .model import DictionaryElementValidatorAssignmentModel, DictionaryElementValidatorAssignmentCollection
from .modelui import DictionaryElementValidatorAssignmentModelUI, DictionaryElementValidatorAssignmentCollectionUI


@App.permission_rule(model=DictionaryElementValidatorAssignmentCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=DictionaryElementValidatorAssignmentModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=DictionaryElementValidatorAssignmentCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=DictionaryElementValidatorAssignmentModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
