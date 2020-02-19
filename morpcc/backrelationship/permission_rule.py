from morpfw.crud import permission as crudperm
from ..app import App
from .model import BackRelationshipModel, BackRelationshipCollection
from .modelui import BackRelationshipModelUI, BackRelationshipCollectionUI


@App.permission_rule(model=BackRelationshipCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=BackRelationshipModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=BackRelationshipCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=BackRelationshipModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
