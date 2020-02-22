import morpfw
from .schema import EntityConstraintSchema


class EntityConstraintModel(morpfw.Model):
    schema = EntityConstraintSchema


class EntityConstraintCollection(morpfw.Collection):
    schema = EntityConstraintSchema
