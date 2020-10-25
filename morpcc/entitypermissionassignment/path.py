from ..app import App
from .model import EntityPermissionAssignmentModel, EntityPermissionAssignmentCollection
# 
from .modelui import EntityPermissionAssignmentModelUI, EntityPermissionAssignmentCollectionUI
# 
from .storage import EntityPermissionAssignmentStorage


def get_collection(request):
    storage = EntityPermissionAssignmentStorage(request)
    return EntityPermissionAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EntityPermissionAssignmentCollection,
          path='/api/v1/entitypermissionassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityPermissionAssignmentModel,
          path='/api/v1/entitypermissionassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


@App.path(model=EntityPermissionAssignmentCollectionUI,
          path='/entitypermissionassignment')
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=EntityPermissionAssignmentModelUI,
          path='/entitypermissionassignment/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

# 
