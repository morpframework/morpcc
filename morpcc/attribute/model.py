from datetime import date, datetime

import morpfw
import rulez
from deform.widget import TextAreaWidget

from ..deform.refdatawidget import ReferenceDataWidget
from ..deform.richtextwidget import RichTextWidget
from ..preparer.html import HTMLSanitizer
from ..validator.refdata import ReferenceDataValidator
from .modelui import AttributeCollectionUI, AttributeModelUI
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

    def ui(self):
        return AttributeModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def datatype(self):
        key = self["type"]
        return DATATYPE_MAPPING[key]["type"]

    @morpfw.requestmemoize()
    def field_metadata(self):
        metadata = {
            "title": self["title"],
            "description": self["description"],
            "required": self["required"],
            "validators": [],
        }

        if self["primary_key"]:
            metadata["index"] = True

        if self["allow_invalid"]:
            metadata["required"] = False

        if not self["allow_invalid"]:
            for v in self.validators():
                metadata["validators"].append(v.field_validator())

        de = self.dictionaryelement()
        if de and not self["allow_invalid"]:
            for v in de.validators():
                metadata["validators"].append(v.field_validator())

        if self["default_factory"]:
            factory_name = self["default_factory"]
            factory = self.request.app.config.default_factory_registry.get(
                factory_name, self.request
            )
            metadata["default_factory"] = factory

        if self["type"] == "string":
            if de and de["referencedata_name"]:
                metadata["deform.widget"] = ReferenceDataWidget(
                    de["referencedata_name"], de["referencedata_property"]
                )
                if not self["allow_invalid"]:
                    metadata["validators"].append(
                        ReferenceDataValidator(
                            de["referencedata_name"], de["referencedata_property"]
                        )
                    )
                return metadata
        if self["type"] == "text":
            metadata.update({"format": "text", "deform.widget": TextAreaWidget()})
            return metadata
        if self["type"] == "richtext":
            metadata.update(
                {
                    "format": "text/html",
                    "preparers": [HTMLSanitizer()],
                    "deform.widget": RichTextWidget(),
                }
            )
            return metadata

        return metadata

    @morpfw.requestmemoize()
    def entity(self):
        col = self.request.get_collection("morpcc.entity")
        dm = col.get(self["entity_uuid"])
        return dm

    @morpfw.requestmemoize()
    def dictionaryelement(self):
        col = self.request.get_collection("morpcc.dictionaryelement")
        dictel = col.get(self["dictionaryelement_uuid"])
        return dictel

    @morpfw.requestmemoize()
    def validators(self):
        col = self.request.get_collection("morpcc.attributevalidatorassignment")
        assignments = col.search(rulez.field["attribute_uuid"] == self.uuid)
        validators = [a.validator() for a in assignments]

        return validators


class AttributeCollection(morpfw.Collection):
    schema = AttributeSchema

    def ui(self):
        return AttributeCollectionUI(self.request, self)
