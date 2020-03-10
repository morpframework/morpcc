def valid_assignment(request, data, mode=None):
    attrcol = request.get_collection("morpcc.attribute")
    valcol = request.get_collection("morpcc.attributevalidator")

    attr = attrcol.get(data["attribute_uuid"])
    validator = valcol.get(data["attributevalidator_uuid"])

    if attr["type"] != validator["type"]:
        return {
            "field": "attributevalidator_uuid",
            "message": "Validator data type mismatch. Expected {}, received {}".format(
                attr["type"], validator["type"]
            ),
        }
