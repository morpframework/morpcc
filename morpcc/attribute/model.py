from datetime import date, datetime

import morpfw
from deform.widget import RichTextWidget, TextAreaWidget

from .schema import ACCEPTED_TYPES, AttributeSchema

DATATYPE_MAPPING = {
    "string": {"type": str, "label": "String"},
    "text": {"type": str, "label": "Text"},
    "richtext": {"type": str, "label": "Rich Text"},
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

    def field_metadata(self):
        if self["type"] == "text":
            return {"format": "text", "deform.widget": TextAreaWidget()}
        if self["type"] == "richtext":
            return {"format": "text", "deform.widget": RichTextWidget()}
        return {}

    def entity(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.entity", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        dm = col.get(self["entity_uuid"])
        return dm


class AttributeCollection(morpfw.Collection):
    schema = AttributeSchema
