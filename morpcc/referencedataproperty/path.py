from ..app import App
from .model import ReferenceDataPropertyModel, ReferenceDataPropertyCollection

#
from .modelui import ReferenceDataPropertyModelUI, ReferenceDataPropertyCollectionUI

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


def get_collection_ui(request):
    col = get_collection(request)
    return ReferenceDataPropertyCollectionUI(request, col)


@App.path(model=ReferenceDataPropertyCollectionUI, path="/referencedataproperty")
def _get_collection_ui(request):
    return get_collection_ui(request)


def get_model_ui(request, identifier):
    col = get_collection(request)
    model = get_model(request, identifier)
    return ReferenceDataPropertyModelUI(
        request, model, ReferenceDataPropertyCollectionUI(request, col)
    )


@App.path(
    model=ReferenceDataPropertyModelUI, path="/referencedataproperty/{identifier}"
)
def _get_model_ui(request, identifier):
    return get_model_ui(request, identifier)


#

