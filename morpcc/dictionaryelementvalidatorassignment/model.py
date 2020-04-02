import morpfw
import rulez

from .modelui import (
    DictionaryElementValidatorAssignmentCollectionUI,
    DictionaryElementValidatorAssignmentModelUI,
)
from .schema import DictionaryElementValidatorAssignmentSchema


class DictionaryElementValidatorAssignmentModel(morpfw.Model):
    schema = DictionaryElementValidatorAssignmentSchema

    def ui(self):
        return DictionaryElementValidatorAssignmentModelUI(
            self.request, self, self.collection.ui()
        )

    @morpfw.requestmemoize()
    def validator(self):
        col = self.request.get_collection("morpcc.attributevalidator")
        res = col.search(rulez.field["name"] == self["attributevalidator_name"])
        if res:
            return res[0]

        return None

    @morpfw.requestmemoize()
    def dictionaryelement(self):
        col = self.request.get_collection("morpcc.dictionaryelement")
        return col.get(self["dictionaryelement_uuid"])


class DictionaryElementValidatorAssignmentCollection(morpfw.Collection):
    schema = DictionaryElementValidatorAssignmentSchema

    def ui(self):
        return DictionaryElementValidatorAssignmentCollectionUI(self.request, self)
