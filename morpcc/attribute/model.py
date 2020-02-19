import morpfw
from .schema import AttributeSchema
from .schema import ACCEPTED_TYPES
from datetime import date, datetime

DATATYPE_MAPPING = {
    "string": {"type": str, "label": "String"},
    "integer": {"type": int, "label": "Integer"},
    "biginteger": {"type": int, "label": "Big Integer"},
    "float": {"type": float, "label": "Float"},
    "double": {"type": float, "label": "Double"},
    "date": {"type": date, "label": "Date"},
    "datetime": {"type": datetime, "label": "DateTime"},
}


class AttributeModel(morpfw.Model):
    schema = AttributeSchema

    def datatype(self):
        key = self["type"]
        return DATATYPE_MAPPING[key]["type"]

    def datamodel(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.datamodel", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        dm = col.get(self["datamodel_uuid"])
        return dm


class AttributeCollection(morpfw.Collection):
    schema = AttributeSchema
