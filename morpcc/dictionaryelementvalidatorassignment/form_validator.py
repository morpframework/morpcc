import rulez


def valid_assignment(request, schema, data, mode=None, **kw):
    ddelcol = request.get_collection("morpcc.dictionaryelement")
    valcol = request.get_collection("morpcc.attributevalidator")

    ddel = ddelcol.get(data["dictionaryelement_uuid"])

    res = valcol.search(rulez.field["name"] == data["attributevalidator_name"])
    if not res:
        return {"field": "attributevalidator_name", "message": "Invalid validator name"}

    validator = res[0]

    if ddel["type"] != validator["type"]:
        return {
            "field": "attributevalidator_name",
            "message": "Validator data type mismatch. Expected {}, received {}".format(
                ddel["type"], validator["type"]
            ),
        }
