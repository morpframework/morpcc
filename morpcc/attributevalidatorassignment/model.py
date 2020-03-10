import morpfw

from .schema import AttributeValidatorAssignmentSchema


class AttributeValidatorAssignmentModel(morpfw.Model):
    schema = AttributeValidatorAssignmentSchema

    def validator(self):
        col = self.request.get_collection("morpcc.attributevalidator")
        return col.get(self["attributevalidator_uuid"])

    def attribute(self):
        col = self.request.get_collection("morpcc.attribute")
        return col.get(self["attribute_uuid"])


class AttributeValidatorAssignmentCollection(morpfw.Collection):
    schema = AttributeValidatorAssignmentSchema
