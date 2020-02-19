import morpfw
from .schema import AttributeConstraintSchema


class AttributeConstraintModel(morpfw.Model):
    schema = AttributeConstraintSchema


class AttributeConstraintCollection(morpfw.Collection):
    schema = AttributeConstraintSchema
