import morpfw
from .schema import SchemaSchema


class SchemaModel(morpfw.Model):
    schema = SchemaSchema


class SchemaCollection(morpfw.Collection):
    schema = SchemaSchema
