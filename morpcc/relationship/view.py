import rulez
from morpfw.crud import permission as crudperms

from ..app import App
from .modelui import RelationshipCollectionUI


def _attribute_search(context, request):
    # FIXME: this need to be secured
    entity_resource_type = "morpcc.entity"
    attribute_resource_type = "morpcc.attribute"
    schema_resource_type = "morpcc.schema"

    schema_uuid = request.GET.get("schema_uuid", "").strip()
    if not schema_uuid:
        return {}

    value_field = request.GET.get("value_field", "").strip()
    if not value_field:
        return {}

    term = request.GET.get("term", "").strip()
    if not term:
        return {}

    attrcol = request.get_collection(attribute_resource_type)
    dmcol = request.get_collection(entity_resource_type)

    term = term.split(".")
    if len(term) == 1:
        term.append(None)

    dmterm = term[0]
    attrterm = term[1]

    dms = dmcol.search(
        query=rulez.and_(
            {"field": "title", "operator": "~", "value": dmterm},
            rulez.field["schema_uuid"] == schema_uuid,
        )
    )

    attrs = []

    for dm in dms:
        query = rulez.field["entity_uuid"] == dm.uuid
        if attrterm:
            query = rulez.and_(
                query, {"field": "title", "operator": "~", "value": attrterm}
            )
        attrs += [(dm, attr) for attr in attrcol.search(query=query)]

    result = {"results": []}
    for dm, attr in attrs:
        text = "{}.{}".format(dm["name"], attr["name"])
        result["results"].append({"id": attr[value_field], "text": text})
    return result


@App.json(
    model=RelationshipCollectionUI, name="attribute-search", permission=crudperms.Search
)
def attribute_search(context, request):
    return _attribute_search(context, request)
