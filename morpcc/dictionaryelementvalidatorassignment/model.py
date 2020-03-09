import morpfw
from .schema import DictionaryElementValidatorAssignmentSchema


class DictionaryElementValidatorAssignmentModel(morpfw.Model):
    schema = DictionaryElementValidatorAssignmentSchema


class DictionaryElementValidatorAssignmentCollection(morpfw.Collection):
    schema = DictionaryElementValidatorAssignmentSchema
