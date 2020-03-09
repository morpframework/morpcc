import morpfw
from .schema import AttributeValidatorAssignmentSchema


class AttributeValidatorAssignmentModel(morpfw.Model):
    schema = AttributeValidatorAssignmentSchema


class AttributeValidatorAssignmentCollection(morpfw.Collection):
    schema = AttributeValidatorAssignmentSchema
