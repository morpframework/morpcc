from ..app import App
from .model import EntityContentIndexQueueModel, EntityContentIndexQueueCollection
# 
from .modelui import EntityContentIndexQueueModelUI, EntityContentIndexQueueCollectionUI
# 
from .storage import EntityContentIndexQueueStorage


def get_collection(request):
    storage = EntityContentIndexQueueStorage(request)
    return EntityContentIndexQueueCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=EntityContentIndexQueueCollection,
          path='/api/v1/entitycontentindexqueue')
def _get_collection(request):
    return get_collection(request)


@App.path(model=EntityContentIndexQueueModel,
          path='/api/v1/entitycontentindexqueue/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


@App.path(model=EntityContentIndexQueueCollectionUI,
          path='/entitycontentindexqueue')
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=EntityContentIndexQueueModelUI,
          path='/entitycontentindexqueue/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

# 
