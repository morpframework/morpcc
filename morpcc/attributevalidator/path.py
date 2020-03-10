from ..app import App
from .model import AttributeValidatorCollection, AttributeValidatorModel

#
from .modelui import AttributeValidatorCollectionUI, AttributeValidatorModelUI

#
from .storage import AttributeValidatorStorage


def get_collection(request):
    storage = AttributeValidatorStorage(request)
    return AttributeValidatorCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=AttributeValidatorCollection, path="/api/v1/attributevalidator")
def _get_collection(request):
    return get_collection(request)


@App.path(model=AttributeValidatorModel, path="/api/v1/attributevalidator/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=AttributeValidatorCollectionUI, path="/attributevalidator")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=AttributeValidatorModelUI, path="/attributevalidator/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
