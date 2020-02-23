import morpfw

from .schema import DictionaryElementSchema


class DictionaryElementModel(morpfw.Model):
    schema = DictionaryElementSchema


class DictionaryElementCollection(morpfw.Collection):
    schema = DictionaryElementSchema
