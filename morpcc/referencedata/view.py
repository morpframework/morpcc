from morpcc.crud.view.listing import listing as default_listing
from morpfw.crud import permission as crudperms

from ..app import App
from .modelui import ReferenceDataCollectionUI, ReferenceEntityUI


@App.html(
    model=ReferenceDataCollectionUI,
    name="listing",
    template="master/referencedata/listing.pt",
    permission=crudperms.Search,
)
def view(context, request):
    return default_listing(context, request)


@App.json(model=ReferenceDataCollectionUI, name="export", permission=crudperms.Search)
def export(context, request):
    result = {}
    for refdata in context.collection.search():

        m = refdata
        result[m["name"]] = {
            "name": m["name"],
            "description": m["description"],
            "keys": {},
        }
        for k in m.referencedatakeys():
            kdata = {"name": k["name"], "description": k["description"], "values": {}}

            for v in k.referencedatavalues():
                kdata["values"][v["property"]] = v["value"]

            result[m["name"]]["keys"][k["name"]] = kdata

    return result
