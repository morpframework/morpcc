from ..app import App
from .model import DataModelContentModel


@App.indexer(model=DataModelContentModel, name="searchabletext")
def searchabletext(context, name):
    datamodel = context.collection.__parent__
    text = []
    for name, attr in datamodel.attributes().items():
        if attr.datatype() == str:
            value = context[name]
            if value:
                text.append(value)
    return " ".join(text)


@App.indexer(model=DataModelContentModel, name="application_uuid")
def application_uuid(context, name):
    return context.collection.__parent__.application().uuid


@App.indexer(model=DataModelContentModel, name="datamodel_uuid")
def datamodel_content_uuid(context, name):
    return context.collection.__parent__.uuid


@App.indexer(model=DataModelContentModel, name="datamodel_content_uuid")
def datamodel_content_uuid(context, name):
    return context.uuid
