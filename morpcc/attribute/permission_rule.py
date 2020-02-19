from morpfw.crud import permission as crudperm
from ..app import App
from .model import AttributeModel, AttributeCollection
from .modelui import AttributeModelUI, AttributeCollectionUI


@App.permission_rule(model=AttributeCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=AttributeModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=AttributeCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=AttributeModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
