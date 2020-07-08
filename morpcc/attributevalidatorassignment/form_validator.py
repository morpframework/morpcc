import rulez


def valid_assignment(request, schema, data, mode=None, **kw):
    attrcol = request.get_collection("morpcc.attribute")
    valcol = request.get_collection("morpcc.attributevalidator")

    attr = attrcol.get(data["attribute_uuid"])
    res = valcol.search(rulez.field["name"] == data["attributevalidator_name"])
    if not res:
        return {"field": "attributevalidator_name", "message": "Invalid Name"}

    validator = res[0]

    if attr["type"] != validator["type"]:
        return {
            "field": "attributevalidator_name",
            "message": "Validator data type mismatch. Expected {}, received {}".format(
                attr["type"], validator["type"]
            ),
        }
