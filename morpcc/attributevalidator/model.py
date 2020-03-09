import morpfw
from .schema import AttributeValidatorSchema


class AttributeValidatorModel(morpfw.Model):
    schema = AttributeValidatorSchema


class AttributeValidatorCollection(morpfw.Collection):
    schema = AttributeValidatorSchema
