from morpfw.crud import permission as crudperm
from ..app import App
from .model import SelectionAttributeModel, SelectionAttributeCollection
from .modelui import SelectionAttributeModelUI, SelectionAttributeCollectionUI


@App.permission_rule(model=SelectionAttributeCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=SelectionAttributeModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=SelectionAttributeCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=SelectionAttributeModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
