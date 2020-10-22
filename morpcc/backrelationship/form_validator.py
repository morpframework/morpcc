def valid_backrelationship(request, schema, data, mode=None, **kw):
    rels = request.get_collection("morpcc.relationship")
    rel = rels.get(data["reference_relationship_uuid"])
    if rel.reference_entity().uuid != data["entity_uuid"]:
        return {
            "field": "reference_relationship_uuid",
            "message": "Invalid relationship. Relationship did not point to the right entity",
        }
