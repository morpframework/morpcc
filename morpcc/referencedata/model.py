import morpfw
import rulez

from ..referencedatakey.path import get_collection as get_keys_collection
from .modelui import ReferenceDataCollectionUI, ReferenceDataModelUI
from .schema import ReferenceDataSchema


class ReferenceDataModel(morpfw.Model):
    schema = ReferenceDataSchema

    def ui(self):
        return ReferenceDataModelUI(self.request, self, self.collection.ui())

    def referencedatakeys(self):
        col = get_keys_collection(self.request)
        return col.search(rulez.field["referencedata_uuid"] == self.uuid)

    def export(self):
        result = {"name": self["name"], "description": self["description"], "keys": {}}
        for k in self.referencedatakeys():
            result["keys"][k["name"]] = k.export()
        return result

    def before_delete(self):
        col = get_keys_collection(self.request)
        for k in col.search(rulez.field["referencedata_uuid"] == self.uuid):
            k.delete()


class ReferenceDataCollection(morpfw.Collection):
    schema = ReferenceDataSchema

    def ui(self):
        return ReferenceDataCollectionUI(self.request, self)
