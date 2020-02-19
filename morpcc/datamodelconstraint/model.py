import morpfw
from .schema import DataModelConstraintSchema


class DataModelConstraintModel(morpfw.Model):
    schema = DataModelConstraintSchema


class DataModelConstraintCollection(morpfw.Collection):
    schema = DataModelConstraintSchema
