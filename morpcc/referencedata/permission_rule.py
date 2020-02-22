from morpfw.crud import permission as crudperm
from ..app import App
from .model import ReferenceEntity, ReferenceDataCollection
from .modelui import ReferenceEntityUI, ReferenceDataCollectionUI


@App.permission_rule(model=ReferenceDataCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=ReferenceEntity,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=ReferenceDataCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=ReferenceEntityUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
