import json

import deform
import morpfw
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from ..app import App
from ..entitycontent.modelui import EntityContentCollectionUI, EntityContentModelUI
from ..util import dataclass_to_colander
from .modelui import EntityCollectionUI, EntityModelUI


@App.html(
    model=EntityCollectionUI,
    name="listing",
    template="master/entity/listing.pt",
    permission=crudperm.View,
)
def listing(context, request):
    result = default_listing(context, request)
    return result


@App.json(model=EntityCollectionUI, name="ajax-status", permission=crudperm.View)
def need_update(context, request):
    dbsync = DatabaseSyncAdapter(context.collection, request)
    return {"need_update": dbsync.need_update()}


@App.html(
    model=EntityModelUI,
    name="edit",
    template="master/entity/edit.pt",
    permission=crudperm.Edit,
)
def edit(context, request):
    return default_edit(context, request)


@App.html(
    model=EntityModelUI,
    name="view",
    template="master/entity/view.pt",
    permission=crudperm.View,
)
def view(context, request):
    result = default_view(context, request)
    # list down columns
    return result


@App.json(model=EntityModelUI, name="term-search", permission=crudperm.View)
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

    col = context.model.content_collection()
    objs = col.search(query={"field": term_field, "operator": "~", "value": term})
    result = {"results": []}
    for obj in objs:
        result["results"].append({"id": obj[value_field], "text": obj[term_field]})
    return result


@App.html(
    model=EntityContentModelUI,
    name="view",
    template="master/entity/content/view.pt",
    permission=crudperm.View,
)
def content_view(context, request):
    result = default_view(context, request)
    result["relationships"] = []
    for r, rel in sorted(context.model.relationships().items(), key=lambda x: x[0]):
        relmodel = rel.resolve_relationship(context.model)
        if relmodel:
            colui = EntityContentCollectionUI(request, relmodel.collection)
            relmodelui = EntityContentModelUI(request, relmodel, colui)
            reldata = default_view(relmodelui, request)
            reldata["title"] = rel["title"]
            reldata["context"] = relmodelui
            result["relationships"].append(reldata)
    result["backrelationships"] = []
    for br, brel in sorted(
        context.model.backrelationships().items(), key=lambda x: x[0]
    ):
        refmodel = brel.reference_relationship().entity()
        columns = []
        column_options = []
        for colname, col in refmodel.effective_attributes().items():
            columns.append(colname)
            column_options.append({"name": colname, "orderable": True})
        breldata = {
            "name": brel["name"],
            "uuid": brel["uuid"],
            "title": brel["title"],
            "single_relation": brel["single_relation"] or False,
            "datatable_url": request.link(
                context,
                "backrelationship-search.json?backrelationship_uuid={}".format(
                    brel["uuid"]
                ),
            ),
            "columns": columns,
            "column_options": json.dumps(column_options),
            "content": brel.resolve_relationship(context.model),
        }

        if brel["single_relation"]:
            if breldata["content"]:
                item = breldata["content"][0]
                itemui = item.ui()
                formschema = dataclass_to_colander(
                    item.schema,
                    request=request,
                    include_fields=itemui.view_include_fields,
                    exclude_fields=itemui.view_exclude_fields,
                )
                breldata["form"] = deform.Form(formschema())
                breldata["form_data"] = item.as_dict()
        result["backrelationships"].append(breldata)
    result["backrelationships"] = sorted(
        result["backrelationships"],
        key=lambda x: (0 if x["single_relation"] else 1, x["name"]),
    )
    return result
