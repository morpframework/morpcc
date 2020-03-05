import rulez
from morpcc.crud.view.listing import datatable_search

from ..app import App
from ..entitycontent.model import EntityContentModelUI
from .modelui import BackRelationshipCollectionUI, BackRelationshipModelUI
from .path import get_model as get_backrelationship


def _relationship_search(context, request):
    # FIXME: this need to be secured
    entity_resource_type = "morpcc.entity"
    relationship_resource_type = "morpcc.relationship"
    value_field = request.GET.get("value_field", "").strip()
    if not value_field:
        return {}

    term = request.GET.get("term", "").strip()
    if not term:
        return {}

    entity_uuid = request.GET.get("entity_uuid", "").strip()

    reltypeinfo = request.app.config.type_registry.get_typeinfo(
        name=relationship_resource_type, request=request
    )

    dmtypeinfo = request.app.config.type_registry.get_typeinfo(
        name=entity_resource_type, request=request
    )

    relcol = reltypeinfo["collection_factory"](request)
    dmcol = dmtypeinfo["collection_factory"](request)

    term = term.split(".")
    if len(term) == 1:
        term.append(None)

    dmterm = term[0]
    relterm = term[1]

    dms = dmcol.search(query={"field": "title", "operator": "~", "value": dmterm})
    rels = []

    for dm in dms:
        query = rulez.field["entity_uuid"] == dm.uuid
        if relterm:
            query = rulez.and_(
                query, {"field": "title", "operator": "~", "value": relterm}
            )
        rels += [(dm, rel) for rel in relcol.search(query=query)]

    if entity_uuid:
        newrels = []
        for dm, rel in rels:
            if rel.reference_attribute()["entity_uuid"] == entity_uuid:
                newrels.append((dm, rel))
        rels = newrels

    result = {"results": []}
    for dm, rel in rels:
        text = "{}.{}".format(dm["name"], rel["name"])
        result["results"].append({"id": rel[value_field], "text": text})
    return result


@App.json(model=BackRelationshipCollectionUI, name="relationship-search")
def relationship_search(context, request):
    return _relationship_search(context, request)


@App.json(model=EntityContentModelUI, name="backrelationship-search.json")
def relationship_content_search(context, request):
    brel_uuid = request.GET.get("backrelationship_uuid", "").strip()
    if not brel_uuid:
        return {}

    brel = get_backrelationship(request, brel_uuid)
    rel = brel.reference_relationship()
    attr = rel.reference_attribute()
    collectionui = brel.content_collection().ui()
    return datatable_search(
        collectionui,
        request,
        additional_filters=rulez.field[rel["name"]] == context.model[attr["name"]],
    )
