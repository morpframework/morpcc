import rulez
import morpfw

def unique_attribute(context, request, data, mode=None):
    if mode == "update":
        return

    builtins = [f.lower() for f in context.schema.__dataclass_fields__.keys()]

    if data['name'] in builtins:
        return "Attribute '{}' is reserved for internal use".format(data['name'])

    get_typeinfo = request.app.config.type_registry.get_typeinfo

    attrinfo = get_typeinfo("morpcc.attribute", request)
    relinfo = get_typeinfo("morpcc.relationship", request)
    brelinfo = get_typeinfo("morpcc.backrelationship", request)

    message = "Attribute already exists"

    for info in [attrinfo, relinfo, brelinfo]:
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


def valid_dictionary_element(context, request, data, mode=None):
    from ..dictionaryelement.path import get_model as get_dictionaryelement

    de_uuid = data.get("dictionaryelement_uuid", None)
    if not de_uuid:
        return

    de = get_dictionaryelement(request, de_uuid)

    if data["type"] != de["type"]:
        return "Type does not match data dictionary (expected {})".format(de["type"])
