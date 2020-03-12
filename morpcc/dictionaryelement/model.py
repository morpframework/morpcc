import morpfw
import rulez

from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI
from .schema import DictionaryElementSchema


class DictionaryElementModel(morpfw.Model):
    schema = DictionaryElementSchema

    def ui(self):
        return DictionaryElementModelUI(self.request, self, self.collection.ui())

    def validators(self):
        assignments = self.validator_assignments()
        validators = [a.validator() for a in assignments]
        return validators

    def validator_assignments(self):
        col = self.request.get_collection("morpcc.dictionaryelementvalidatorassignment")
        assignments = col.search(rulez.field["dictionaryelement_uuid"] == self.uuid)
        return assignments

    def before_delete(self):
        for va in self.validator_assignments():
            va.delete()


class DictionaryElementCollection(morpfw.Collection):
    schema = DictionaryElementSchema

    def ui(self):
        return DictionaryElementCollectionUI(self.request, self)
