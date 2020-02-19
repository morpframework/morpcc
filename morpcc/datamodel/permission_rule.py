from morpfw.crud import permission as crudperm

from ..app import App
from .model import (
    DataModelCollection,
    DataModelContentCollection,
    DataModelContentModel,
    DataModelModel,
)
from .modelui import DataModelCollectionUI, DataModelModelUI


@App.permission_rule(model=DataModelCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=DataModelModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


@App.permission_rule(model=DataModelContentCollection, permission=crudperm.All)
def allow_content_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=DataModelContentModel, permission=crudperm.All)
def allow_content_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=DataModelCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=DataModelModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True


#
