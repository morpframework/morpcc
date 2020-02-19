import rulez

from ..app import App
from .modelui import RelationshipCollectionUI


def _attribute_search(context, request):
    # FIXME: this need to be secured
    datamodel_resource_type = "morpcc.datamodel"
    attribute_resource_type = "morpcc.attribute"
    value_field = request.GET.get("value_field", "").strip()
    if not value_field:
        return {}
    term = request.GET.get("term", "").strip()
    if not term:
        return {}

    attrtypeinfo = request.app.config.type_registry.get_typeinfo(
        name=attribute_resource_type, request=request
    )

    dmtypeinfo = request.app.config.type_registry.get_typeinfo(
        name=datamodel_resource_type, request=request
    )

    attrcol = attrtypeinfo["collection_factory"](request)
    dmcol = dmtypeinfo["collection_factory"](request)

    term = term.split(".")
    if len(term) == 1:
        term.append(None)

    dmterm = term[0]
    attrterm = term[1]

    dms = dmcol.search(query={"field": "title", "operator": "~", "value": dmterm})

    attrs = []

    for dm in dms:
        query = rulez.field["datamodel_uuid"] == dm.uuid
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


@App.json(model=RelationshipCollectionUI, name="attribute-search")
def attribute_search(context, request):
    return _attribute_search(context, request)
