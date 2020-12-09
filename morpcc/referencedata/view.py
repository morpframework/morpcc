import json

import rulez
from morpcc.crud.view.listing import listing as default_listing
from morpfw.crud import permission as crudperms

from ..app import App
from ..referencedatakey.path import get_collection as get_refdatakey_collection
from ..referencedataproperty.path import get_collection as get_refdataprop_collection
from .modelui import ReferenceDataCollectionUI, ReferenceDataModelUI
from .path import get_collection as get_refdata_collection


@App.html(
    model=ReferenceDataCollectionUI,
    name="listing",
    template="master/referencedata/listing.pt",
    permission=crudperms.Search,
)
def view(context, request):
    result = default_listing(context, request)
    result["page_title"] = "Reference Data Manager"
    return result


@App.view(model=ReferenceDataCollectionUI, name="export", permission=crudperms.Search)
def export(context, request):
    result = {}
    for refdata in context.collection.search():

        result[refdata["name"]] = refdata.export()

    result = json.dumps(result)

    @request.after
    def set_header(response):
        response.headers.add("Content-Type", "application/json")
        response.headers.add(
            "Content-Disposition", 'attachment; filename="referencedata.json'
        )
        response.headers.add("Content-Length", str(len(result)))

    return result


@App.view(model=ReferenceDataModelUI, name="export", permission=crudperms.Search)
def export_model(context, request):

    result = context.model.export()
    result = json.dumps(result)

    @request.after
    def set_header(response):
        response.headers.add("Content-Type", "application/json")
        response.headers.add(
            "Content-Disposition",
            'attachment; filename="%s.json' % context.model["name"],
        )
        response.headers.add("Content-Length", str(len(result)))

    return result


@App.json(
    model=ReferenceDataCollectionUI,
    name="vocabulary-search",
    permission=crudperms.Search,
)
def vocabulary_search(context, request):
    refdata_name = request.GET.get("name", "").strip()
    if not refdata_name:
        return {}

    refdata_property = request.GET.get("property", "").strip()

    if not refdata_property:
        return {}

    term = request.GET.get("term", "").strip()

    refdatas = get_refdata_collection(request)

    col = get_refdata_collection(request)
    refdatas = col.search(rulez.field["name"] == refdata_name)
    if not refdatas:
        return {}
    refdata = refdatas[0]

    keys = refdata.referencedatakeys()

    key_props = []

    prop_col = get_refdataprop_collection(request)
    for key in keys:
        props = prop_col.search(
            rulez.and_(
                rulez.field["referencedatakey_uuid"] == key.uuid,
                rulez.field["name"] == refdata_property,
                {"field": "value", "operator": "~", "value": term},
            )
        )
        if props:
            prop = props[0]
            key_props.append({"id": key["name"], "text": prop["value"]})

    if not key_props:
        return {}
    return {"results": key_props}
