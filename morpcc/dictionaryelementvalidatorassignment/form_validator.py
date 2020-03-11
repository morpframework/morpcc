def valid_assignment(request, schema, data, mode=None):
    ddelcol = request.get_collection("morpcc.dictionaryelement")
    valcol = request.get_collection("morpcc.attributevalidator")

    ddel = ddelcol.get(data["dictionaryelement_uuid"])
    validator = valcol.get(data["attributevalidator_uuid"])

    if ddel["type"] != validator["type"]:
        return {
            "field": "attributevalidator_uuid",
            "message": "Validator data type mismatch. Expected {}, received {}".format(
                ddel["type"], validator["type"]
            ),
        }
