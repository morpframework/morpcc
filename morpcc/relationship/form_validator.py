def valid_search_attribute(request, schema, data, mode=None, **kw):
    attrs = request.get_collection("morpcc.attribute")
    value_attr = attrs.get(data["reference_attribute_uuid"])
    search_attr = attrs.get(data["reference_search_attribute_uuid"])
    if value_attr.entity().uuid != search_attr.entity().uuid:
        return {
            "field": "reference_search_attribute_uuid",
            "message": "Search attribute must be from the same entity as reference attribute",
        }
