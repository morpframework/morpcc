from ..app import App
from .model import ReferenceDataPropertyCollection, ReferenceDataPropertyModel

#
from .modelui import ReferenceDataPropertyCollectionUI, ReferenceDataPropertyModelUI

#
from .storage import ReferenceDataPropertyStorage


def get_collection(request):
    storage = ReferenceDataPropertyStorage(request)
    return ReferenceDataPropertyCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ReferenceDataPropertyCollection, path="/api/v1/referencedataproperty")
def _get_collection(request):
    return get_collection(request)


@App.path(
    model=ReferenceDataPropertyModel, path="/api/v1/referencedataproperty/{identifier}"
)
def _get_model(request, identifier):
    return get_model(request, identifier)


#


@App.path(model=ReferenceDataPropertyCollectionUI, path="/referencedataproperty")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(
    model=ReferenceDataPropertyModelUI, path="/referencedataproperty/{identifier}"
)
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
