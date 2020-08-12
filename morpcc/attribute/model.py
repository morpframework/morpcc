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
    "boolean": {"type": bool, "label": "Boolean"},
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
        return self._field_metadata()

    @morpfw.requestmemoize()
    def field_metadata_allow_invalid(self):
        return self._field_metadata(allow_invalid=True)

    def _field_metadata(self, allow_invalid=False):
        metadata = {
            "title": self["title"],
            "description": self["description"],
            "required": self["required"],
            "searchable": self["searchable"],
            "validators": [],
        }

        allow_invalid = allow_invalid or self["allow_invalid"]

        if self["primary_key"]:
            metadata["index"] = True

        if allow_invalid:
            metadata["required"] = False

        if not allow_invalid:
            for v in self.validators():
                metadata["validators"].append(v.field_validator())

        rel_collection = self.request.get_collection("morpcc.relationship")
        if rel_collection.search(rulez.field["reference_attribute_uuid"] == self.uuid):
            metadata["index"] = True

        de = self.dictionaryelement()
        if de and not allow_invalid:
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
                    de["referencedata_name"],
                    de["referencedata_property"],
                    placeholder="Select %s" % self["title"],
                )
                if not allow_invalid:
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
        if not self["dictionaryelement_uuid"]:
            return None
        col = self.request.get_collection("morpcc.dictionaryelement")
        dictel = col.get(self["dictionaryelement_uuid"])
        return dictel

    @morpfw.requestmemoize()
    def referencedata(self):
        de = self.dictionaryelement()
        if de:
            return de.referencedata()
        return None

    @morpfw.requestmemoize()
    def referencedata_resolve(self, key):
        de = self.dictionaryelement()
        if de:
            return de.referencedata_resolve(key)
        return None

    @morpfw.requestmemoize()
    def validators(self):
        col = self.request.get_collection("morpcc.attributevalidatorassignment")
        assignments = col.search(rulez.field["attribute_uuid"] == self.uuid)
        validators = [a.validator() for a in assignments if a.validator()]
        ddel = self.dictionaryelement()
        if ddel:
            ddvalidators = self.dictionaryelement().validators()
            validators += ddvalidators
        return validators

    @morpfw.requestmemoize()
    def builtin_validators(self):
        result = []
        if self["required"]:
            result.append(
                {
                    "title": "Required but missing",
                    "description": "This validator checks for missing records (null)",
                    "name": "__required__",
                    "validate": lambda x: x is not None,
                    "error_message": "Field is required",
                }
            )
        if self.referencedata():
            # we do it this way so that pickling will work
            refdata = self.referencedata()
            refdata_validate = refdata.validator()
            result.append(
                {
                    "title": "Reference data non-compliance",
                    "description": "This validator checks for value non-compliance based on configured reference data",
                    "name": "__refdata_compliance__",
                    "validate": refdata_validate,
                    "error_message": "Value does not exists in reference data",
                }
            )
        return result

    @morpfw.requestmemoize()
    def get_validator(self, name):
        for v in self.validators():
            if v["name"] == name:
                return v

    @morpfw.requestmemoize()
    def get_builtin_validator(self, name):
        for v in self.builtin_validators():
            if v["name"] == name:
                return v


class AttributeCollection(morpfw.Collection):
    schema = AttributeSchema

    def ui(self):
        return AttributeCollectionUI(self.request, self)
