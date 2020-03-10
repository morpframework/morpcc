import morpfw

from .schema import DictionaryElementValidatorAssignmentSchema


class DictionaryElementValidatorAssignmentModel(morpfw.Model):
    schema = DictionaryElementValidatorAssignmentSchema

    def validator(self):
        col = self.request.get_collection("morpcc.attributevalidator")
        return col.get(self["attributevalidator_uuid"])

    def dictionaryelement(self):
        col = self.request.get_collection("morpcc.dictionaryelement")
        return col.get(self["dictionaryelement_uuid"])


class DictionaryElementValidatorAssignmentCollection(morpfw.Collection):
    schema = DictionaryElementValidatorAssignmentSchema
