import morpfw
import rulez


def unique_attribute(request, data, mode=None):
    if mode == "update":
        return

    builtins = [f.lower() for f in morpfw.Schema.__dataclass_fields__.keys()]

    if data["name"] in builtins:
        return {
            "field": "name",
            "message": "Attribute '{}' is reserved for internal use".format(
                data["name"]
            ),
        }

    message = "Attribute already exists"

    for restype in [
        "morpcc.attribute",
        "morpcc.relationship",
        "morpcc.backrelationship",
    ]:
        col = request.get_collection(restype)
        if col.search(
            rulez.and_(
                rulez.field["name"] == data["name"],
                rulez.field["entity_uuid"] == data["entity_uuid"],
            )
        ):
            return {"field": "name", "message": message}


def required_if_primary_key(request, data, mode=None):
    if data["primary_key"]:
        if not data["required"]:
            return {
                "field": "required",
                "message": "Primary key must be set to required",
            }


def valid_dictionary_element(request, data, mode=None):

    de_uuid = data.get("dictionaryelement_uuid", None)
    if not de_uuid:
        return

    col = request.get_collection("morpcc.dictionaryelement")
    de = col.get(de_uuid)

    if data["type"] != de["type"]:
        return {
            "field": "type",
            "message": "Type does not match data dictionary (expected {})".format(
                de["type"]
            ),
        }
