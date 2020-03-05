from morpfw.crud import permission as crudperm
from ..app import App
from .model import SchemaModel, SchemaCollection
from .modelui import SchemaModelUI, SchemaCollectionUI


@App.permission_rule(model=SchemaCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=SchemaModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=SchemaCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=SchemaModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
