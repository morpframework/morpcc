from ..app import App
from .model import (
    EntityContentCollection,
    EntityContentModel,
    content_collection_factory,
)
from .modelui import EntityContentCollectionUI, EntityContentModelUI


def get_content_collection(
    request, appidentifier, entityidentifier
) -> EntityContentCollection:
    entity = request.get_collection("morpcc.entity").get(entityidentifier)
    applicaton = request.get_collection("morpcc.application").get(appidentifier)
    return content_collection_factory(entity, applicaton)


@App.path(
    model=EntityContentCollection,
    path="/api/v1/application/{identifier}/entity/{entityidentifier}/records",
    variables=lambda obj: {
        "identifier": obj.__application__.identifier,
        "entityidentifier": obj.__parent__.identifier,
    },
)
def _get_collection(request, identifier, entityidentifier):
    return get_content_collection(request, identifier, entityidentifier)


@App.path(
    model=EntityContentModel,
    path="/api/v1/application/{identifier}/entity/{entityidentifier}/records/{recordidentifier}",
    variables=lambda obj: {
        "identifier": obj.collection.__application__.identifier,
        "entityidentifier": obj.collection.__parent__.identifier,
        "recordidentifier": obj.identifier,
    },
)
def _get_content_model(request, identifier, entityidentifier, recordidentifier):
    col = get_content_collection(request, identifier, entityidentifier)
    return col.get(recordidentifier)


@App.path(
    model=EntityContentCollectionUI,
    path="/application/{identifier}/entity/{entityidentifier}/records/",
    variables=lambda obj: {
        "identifier": obj.collection.__application__.identifier,
        "entityidentifier": obj.collection.__parent__.identifier,
    },
)
def get_model_content_collection_ui(request, identifier, entityidentifier):
    col = get_content_collection(request, identifier, entityidentifier)
    return col.ui()


@App.path(
    model=EntityContentModelUI,
    path="/application/{identifier}/entity/{entityidentifier}/records/{recordidentifier}",
    variables=lambda obj: {
        "identifier": obj.collection_ui.collection.__application__.identifier,
        "entityidentifier": obj.collection_ui.collection.__parent__.identifier,
        "recordidentifier": obj.model.identifier,
    },
)
def get_model_content_model(request, identifier, entityidentifier, recordidentifier):
    col = get_content_collection(request, identifier, entityidentifier)
    return col.ui().get(recordidentifier)
