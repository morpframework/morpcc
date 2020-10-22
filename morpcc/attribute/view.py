from dataclasses import field

import rulez
from morpcc.crud.view.edit import edit as default_edit
from morpfw import request
from morpfw.crud import permission as crudperm

from ..app import App
from .modelui import AttributeCollectionUI, AttributeModelUI


@App.html(
    model=AttributeModelUI,
    name="edit",
    template="master/attribute/edit.pt",
    permission=crudperm.Edit,
)
def edit(context, request):
    return default_edit(context, request)


@App.json(
    model=AttributeCollectionUI,
    name="reorder",
    request_method="POST",
    permission=crudperm.Edit,
)
def reorder(context, request):
    mapping = request.json["mapping"]
    collection = context.collection
    attrs = collection.search(
        rulez.field["entity_uuid"] == request.GET.get("entity_uuid"),
        order_by=("order", "asc"),
    )
    attrs = list(sorted(attrs, key=lambda x: [x["order"], x["created"]]))
    count = 0
    field_orders = {}
    for attr in attrs:
        field_orders[attr["name"]] = {"order": count, "obj": attr}
        count += 1
    new_mapping = []
    for m in mapping:
        # ord_old = field_orders[m["old"]]["order"]
        ord_new = field_orders[m["new"]]["order"]

        new_mapping.append((m["old"], ord_new))

    for no in new_mapping:
        field_orders[no[0]]["order"] = no[1]

    for fo in field_orders.values():
        if fo["order"] != fo["obj"]["order"]:
            fo["obj"].update({"order": fo["order"]}, deserialize=False)

    return {}
