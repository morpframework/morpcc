from morpfw.crud import permission as crudperm
from ..app import App
from .model import DataModelConstraintModel, DataModelConstraintCollection
from .modelui import DataModelConstraintModelUI, DataModelConstraintCollectionUI


@App.permission_rule(model=DataModelConstraintCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=DataModelConstraintModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=DataModelConstraintCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=DataModelConstraintModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
