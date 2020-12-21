import json

import colander
import deform
import rulez
from inverter import dc2colander
from morpfw.crud import permission as crudperm

from ..app import App
from ..application.model import ApplicationModel
from ..crud.view.edit import edit as default_edit
from ..crud.view.listing import datatable_search
from ..crud.view.listing import listing as default_listing
from ..crud.view.view import view as default_view
from ..util import validate_form
from ..validator.refdata import ReferenceDataValidator
from .model import content_collection_factory
from .modelui import EntityContentCollectionUI, EntityContentModelUI


@App.json(model=EntityContentCollectionUI, name="term-search", permission=crudperm.View)
def term_search(context, request):
    value_field = request.GET.get("value_field", "").strip()
    if not value_field:
        return {}
    term_field = request.GET.get("term_field", "").strip()
    if not term_field:
        return {}
    term = request.GET.get("term", "").strip()
    if not term:
        return {}

    col = context.collection
    objs = col.search(query={"field": term_field, "operator": "~", "value": term})
    result = {"results": []}
    for obj in objs:
        result["results"].append({"id": obj[value_field], "text": obj[term_field]})
    return result


@App.html(
    model=EntityContentModelUI,
    name="view",
    template="master/crud/view.pt",
    permission=crudperm.View,
)
def content_view(context, request):
    result = default_view(context, request)
    for refdata in result["references"]:
        item = refdata["content"].model
        validate_form(request, item, item.schema, refdata["form"])
    for brefdata in result["single_backreferences"]:
        item = brefdata["content"].model
        validate_form(
            request, item, item.schema, brefdata["form"],
        )

    item = result["content"].model
    validate_form(request, item, item.schema, result["form"])
    return result


def _entity_dt_result_render(context, request, columns, objs):
    rows = []
    collection = context.collection
    for o in objs:
        row = []
        formschema = dc2colander.convert(
            collection.schema, request=request, default_tzinfo=request.timezone()
        )
        fs = formschema()
        fs = fs.bind(context=o, request=request)
        form = deform.Form(fs)
        validate_form(request, o, o.schema, form)
        for c in columns:
            if c["name"].startswith("structure:"):
                row.append(context.get_structure_column(o, request, c["name"]))
            else:
                field = form[c["name"]]
                value = o.data[c["name"]]
                if value is None:
                    value = colander.null
                out = field.render(
                    value, readonly=True, request=request, context=context
                )
                if field.error:
                    for msg in field.error.messages():
                        out += (
                            "<div class='alert alert-danger'>"
                            "<i class='fa fa-exclamation-triangle'></i>"
                            " {}</div>"
                        ).format(msg)
                row.append(out)
        rows.append(row)
    return rows


def _relationship_content_search(context, request, request_method="GET"):
    bref_name = request.GET.get("backreference_name", "").strip()
    if not bref_name:
        return {}

    bref = None
    for br in context.schema.__backreferences__:
        if br.name == bref_name:
            bref = br
            break

    ref = bref.get_reference(request)
    collection = bref.collection(request)
    collectionui = collection.ui()

    return datatable_search(
        collectionui,
        request,
        additional_filters=rulez.field(ref.name) == context.model[ref.attribute],
        renderer=_entity_dt_result_render,
        request_method=request_method,
    )


@App.json(
    model=EntityContentModelUI,
    name="backreference-search.json",
    permission=crudperm.View,
)
def relationship_content_search(context, request):
    return _relationship_content_search(context, request)


@App.json(
    model=EntityContentModelUI,
    name="backreference-search.json",
    request_method="POST",
    permission=crudperm.View,
)
def relationship_content_search_post(context, request):
    return _relationship_content_search(context, request, request_method="POST")

