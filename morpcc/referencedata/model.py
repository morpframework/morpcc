import morpfw
import rulez

from ..referencedatakey.path import get_collection as get_keys_collection
from .modelui import ReferenceDataCollectionUI, ReferenceDataModelUI
from .schema import ReferenceDataSchema


class ReferenceDataModel(morpfw.Model):
    schema = ReferenceDataSchema

    def ui(self):
        return ReferenceDataModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def referencedatakeys(self):
        col = get_keys_collection(self.request)
        return col.search(rulez.field["referencedata_uuid"] == self.uuid)

    @morpfw.requestmemoize()
    def lookup_key(self, key):
        col = self.request.get_collection("morpcc.referencedatakey")
        res = col.search(
            rulez.and_(
                rulez.field["referencedata_uuid"] == self.uuid,
                rulez.field["name"] == key,
            )
        )
        if res:
            return res[0]
        return None

    def export(self):
        result = {"name": self["name"], "description": self["description"], "keys": {}}
        for k in self.referencedatakeys():
            result["keys"][k["name"]] = k.export()
        return result

    def validator(self):
        refdata = self.export()

        def refdata_validate(value):
            if value is None:
                return True
            marker = object()
            properties = refdata["keys"].get(value, marker)
            if properties is marker:
                return False
            return True

        return refdata_validate

    def before_delete(self):
        for k in self.referencedatakeys():
            k.delete()
        return super().before_delete()


class ReferenceDataCollection(morpfw.Collection):
    schema = ReferenceDataSchema

    def ui(self):
        return ReferenceDataCollectionUI(self.request, self)
