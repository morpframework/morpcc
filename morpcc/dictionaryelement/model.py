import morpfw
import rulez

from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI
from .schema import DictionaryElementSchema


class DictionaryElementModel(morpfw.Model):
    schema = DictionaryElementSchema

    def ui(self):
        return DictionaryElementModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def validators(self):
        assignments = self.validator_assignments()
        validators = [a.validator() for a in assignments]
        return validators

    @morpfw.requestmemoize()
    def validator_assignments(self):
        col = self.request.get_collection("morpcc.dictionaryelementvalidatorassignment")
        assignments = col.search(rulez.field["dictionaryelement_uuid"] == self.uuid)
        return assignments

    @morpfw.requestmemoize()
    def referencedata(self):
        if not self["referencedata_name"]:
            return None
        col = self.request.get_collection("morpcc.referencedata")
        res = col.search(rulez.field["name"] == self["referencedata_name"])
        if res:
            return res[0]
        return None

    @morpfw.requestmemoize()
    def referencedata_resolve(self, key):
        refdata = self.referencedata()
        if not refdata:
            return None
        rdkey = refdata.lookup_key(key)
        if not rdkey:
            return None
        rdprop = rdkey.lookup_property(self["referencedata_property"])
        if not rdprop:
            return None
        return rdprop["value"]

    def before_delete(self):
        for va in self.validator_assignments():
            va.delete()
        return super().before_delete()


class DictionaryElementCollection(morpfw.Collection):
    schema = DictionaryElementSchema

    def ui(self):
        return DictionaryElementCollectionUI(self.request, self)
