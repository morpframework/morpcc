from morpfw.crud import permission as crudperm

from ..app import App
from .model import DictionaryElementCollection, DictionaryElementModel
from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI


@App.permission_rule(model=DictionaryElementCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=DictionaryElementModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=DictionaryElementCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=DictionaryElementModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

#

