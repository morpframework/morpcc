from morpfw.crud import permission as crudperm
from ..app import App
from .model import EntityConstraintModel, EntityConstraintCollection
from .modelui import EntityConstraintModelUI, EntityConstraintCollectionUI


@App.permission_rule(model=EntityConstraintCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=EntityConstraintModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=EntityConstraintCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=EntityConstraintModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
