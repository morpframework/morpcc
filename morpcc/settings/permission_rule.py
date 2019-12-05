from morpfw.crud import permission as crudperm
from ..app import App
from .model import SettingModel, SettingCollection
from .modelui import SettingModelUI, SettingCollectionUI


@App.permission_rule(model=SettingCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=SettingModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=SettingCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=SettingModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
