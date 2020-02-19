from morpfw.crud import permission as crudperm
from ..app import App
from .model import IndexModel, IndexCollection
from .modelui import IndexModelUI, IndexCollectionUI


@App.permission_rule(model=IndexCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=IndexModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=IndexCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=IndexModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
