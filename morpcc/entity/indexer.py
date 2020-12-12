import re
import string

from inverter.common import dataclass_get_type

from ..app import App
from ..entitycontent.model import EntityContentModel

html_tag = re.compile("<.*?>")


def remove_html_tags(text):
    return re.sub(html_tag, "", text)


@App.indexer(model=EntityContentModel, name="title")
def title(context, name):
    entity = context.collection.__parent__
    application = context.collection.__application__

    return "{} > {} > {}".format(application["title"], entity["title"], context.uuid)


@App.indexer(model=EntityContentModel, name="description")
def description(context, name):
    return None


@App.indexer(model=EntityContentModel, name="index_resolver")
def index_resolver(context, name):
    return "morpcc.entity.content"


@App.indexer(model=EntityContentModel, name="searchabletext")
def searchabletext(context, name):
    entity = context.collection.__parent__
    text = []
    for name, attr in entity.dataclass(
        context.application().uuid
    ).__dataclass_fields__.items():
        dctype = dataclass_get_type(attr)
        if dctype["type"] == str:
            dformat = dctype["metadata"].get("format", None)
            if dformat == "uuid":
                continue

            value = context[name]

            if dformat == "text/html":
                value = remove_html_tags(value)

            if value:
                text.append(value.lower())
    searchabletext = " ".join(text)
    searchabletext = searchabletext.translate(
        str.maketrans("", "", string.punctuation)
    ).lower()
    return searchabletext


@App.indexer(model=EntityContentModel, name="application_uuid")
def application_uuid(context, name):
    return context.collection.__application__.uuid


@App.indexer(model=EntityContentModel, name="entity_uuid")
def entity_uuid(context, name):
    return context.collection.__parent__.uuid


@App.indexer(model=EntityContentModel, name="entity_content_uuid")
def entity_content_uuid(context, name):
    return context.uuid
