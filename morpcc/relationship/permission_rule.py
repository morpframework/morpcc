from morpfw.crud import permission as crudperm
from ..app import App
from .model import RelationshipModel, RelationshipCollection
from .modelui import RelationshipModelUI, RelationshipCollectionUI


@App.permission_rule(model=RelationshipCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=RelationshipModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=RelationshipCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=RelationshipModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
