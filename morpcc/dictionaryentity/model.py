import morpfw
import rulez

from .modelui import DictionaryEntityCollectionUI, DictionaryEntityModelUI
from .schema import DictionaryEntitySchema


class DictionaryEntityModel(morpfw.Model):
    schema = DictionaryEntitySchema

    def ui(self):
        return DictionaryEntityModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def dictionary_elements(self):
        col = self.request.get_collection("morpcc.dictionaryelement")
        return col.search(rulez.field["dictionaryentity_uuid"] == self.uuid)

    def before_delete(self):
        for el in self.dictionary_elements():
            el.delete()
        return super().before_delete()


class DictionaryEntityCollection(morpfw.Collection):
    schema = DictionaryEntitySchema

    def ui(self):
        return DictionaryEntityCollectionUI(self.request, self)
