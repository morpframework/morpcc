import morpfw
import rulez

from .modelui import (
    AttributeValidatorAssignmentCollectionUI,
    AttributeValidatorAssignmentModelUI,
)
from .schema import AttributeValidatorAssignmentSchema


class AttributeValidatorAssignmentModel(morpfw.Model):
    schema = AttributeValidatorAssignmentSchema

    def ui(self):
        return AttributeValidatorAssignmentModelUI(
            self.request, self, self.collection.ui()
        )

    @morpfw.requestmemoize()
    def validator(self):
        col = self.request.get_collection("morpcc.attributevalidator")
        validators = col.search(rulez.field["name"] == self["attributevalidator_name"])
        if validators:
            return validators[0]
        return None

    @morpfw.requestmemoize()
    def attribute(self):
        col = self.request.get_collection("morpcc.attribute")
        return col.get(self["attribute_uuid"])


class AttributeValidatorAssignmentCollection(morpfw.Collection):
    schema = AttributeValidatorAssignmentSchema

    def ui(self):
        return AttributeValidatorAssignmentCollectionUI(self.request, self)
