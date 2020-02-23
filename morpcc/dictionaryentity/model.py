import morpfw
from .schema import DictionaryEntitySchema


class DictionaryEntityModel(morpfw.Model):
    schema = DictionaryEntitySchema


class DictionaryEntityCollection(morpfw.Collection):
    schema = DictionaryEntitySchema
