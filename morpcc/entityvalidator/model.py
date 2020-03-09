import morpfw
from .schema import EntityValidatorSchema


class EntityValidatorModel(morpfw.Model):
    schema = EntityValidatorSchema


class EntityValidatorCollection(morpfw.Collection):
    schema = EntityValidatorSchema
