import rulez


def unique_attribute(context, request, data, mode=None):
    if mode == "update":
        return

    get_typeinfo = request.app.config.type_registry.get_typeinfo

    attrinfo = get_typeinfo("morpcc.attribute", request)
    selattrinfo = get_typeinfo("morpcc.selectionattribute", request)
    relinfo = get_typeinfo("morpcc.relationship", request)
    brelinfo = get_typeinfo("morpcc.backrelationship", request)

    message = "Attribute already exists"

    for info in [attrinfo, selattrinfo, relinfo, brelinfo]:
        col = info["collection_factory"](request)
        if col.search(
            rulez.and_(
                rulez.field["name"] == data["name"],
                rulez.field["entity_uuid"] == data["entity_uuid"],
            )
        ):
            return message


def required_if_primary_key(context, request, data, mode=None):
    if data["primary_key"]:
        if not data["required"]:
            return "Primary key must be set to required"
