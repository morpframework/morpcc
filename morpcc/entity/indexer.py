import deform
from morpfw.crud.schemaconverter.common import dataclass_get_type
from morpfw.crud.schemaconverter.dataclass2colander import \
    dataclass_to_colander

from ..app import App
from .model import EntityContentModel


@App.indexer(model=EntityContentModel, name="title")
def title(context, name):
    entity = context.collection.__parent__
    application = entity.application()

    return "{}/{}/{}".format(application["title"], entity["title"], context.uuid)


@App.indexer(model=EntityContentModel, name="description")
def description(context, name):
    return None


@App.indexer(model=EntityContentModel, name="preview")
def preview(context, name):
    ui = context.ui()
    request = context.request
    formschema = dataclass_to_colander(
        context.schema,
        request=request,
        include_fields=ui.view_include_fields,
        exclude_fields=ui.view_exclude_fields,
    )
    form = deform.Form(formschema())
    form_data = context.data.as_dict()
    return form.render(appstruct=form_data, readonly=True, request=request, context=ui)


@App.indexer(model=EntityContentModel, name="index_resolver")
def index_resolver(context, name):
    return "morpcc.entity.content"


@App.indexer(model=EntityContentModel, name="searchabletext")
def searchabletext(context, name):
    entity = context.collection.__parent__
    text = []
    for name, attr in entity.dataclass().__dataclass_fields__.items():
        dctype = dataclass_get_type(attr)
        if dctype["type"] == str:
            if dctype["metadata"].get("format", None) == "uuid":
                continue
            print(name, context[name])
            value = context[name]
            if value:
                text.append(value.lower())
    return " ".join(text)


@App.indexer(model=EntityContentModel, name="application_uuid")
def application_uuid(context, name):
    return context.collection.__parent__.application().uuid


@App.indexer(model=EntityContentModel, name="entity_uuid")
def entity_content_uuid(context, name):
    return context.collection.__parent__.uuid


@App.indexer(model=EntityContentModel, name="entity_content_uuid")
def entity_content_uuid(context, name):
    return context.uuid
