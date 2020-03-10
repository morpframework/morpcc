import morpfw

from .modelui import DictionaryEntityCollectionUI, DictionaryEntityModelUI
from .schema import DictionaryEntitySchema


class DictionaryEntityModel(morpfw.Model):
    schema = DictionaryEntitySchema

    def ui(self):
        return DictionaryEntityModelUI(self.request, self, self.collection.ui())


class DictionaryEntityCollection(morpfw.Collection):
    schema = DictionaryEntitySchema

    def ui():
        return DictionaryEntityCollectionUI(self.request, self)
