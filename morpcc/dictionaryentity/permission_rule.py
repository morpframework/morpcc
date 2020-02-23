from morpfw.crud import permission as crudperm
from ..app import App
from .model import DictionaryEntityModel, DictionaryEntityCollection
from .modelui import DictionaryEntityModelUI, DictionaryEntityCollectionUI


@App.permission_rule(model=DictionaryEntityCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=DictionaryEntityModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=DictionaryEntityCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=DictionaryEntityModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
