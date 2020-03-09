from morpfw.crud import permission as crudperm
from ..app import App
from .model import ReferenceDataModel, ReferenceDataCollection
from .modelui import ReferenceDataModelUI, ReferenceDataCollectionUI


@App.permission_rule(model=ReferenceDataCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=ReferenceDataModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


#


@App.permission_rule(model=ReferenceDataCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=ReferenceDataModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True


#

