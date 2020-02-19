from ..app import App
from .modelui import ReferenceDataModelUI
from .modelui import ReferenceDataCollectionUI
from morpcc.crud.view.listing import listing as default_listing
from morpfw.crud import permission as crudperms


@App.html(
    model=ReferenceDataCollectionUI,
    name="listing",
    template="master/referencedata/listing.pt",
    permission=crudperms.Search,
)
def view(context, request):
    return default_listing(context, request)


@App.json(model=ReferenceDataModelUI, name="export", permission=crudperms.Search)
def export(context, request):
    m = context.model
    result = {
        m["name"]: {"name": m["name"], "description": m["description"], "keys": {}}
    }
    for k in m.referencedatakeys():
        kdata = {"name": k["name"], "description": k["description"], "values": {}}

        for v in k.referencedatavalues():
            kdata["values"][v["valtype"]] = v["value"]

        result[m["name"]]["keys"][k["name"]] = kdata

    return result
