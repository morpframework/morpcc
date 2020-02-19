from morpfw.crud import permission as crudperm
from ..app import App
from .model import ReferenceDataKeyModel, ReferenceDataKeyCollection
from .modelui import ReferenceDataKeyModelUI, ReferenceDataKeyCollectionUI


@App.permission_rule(model=ReferenceDataKeyCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=ReferenceDataKeyModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=ReferenceDataKeyCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=ReferenceDataKeyModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
