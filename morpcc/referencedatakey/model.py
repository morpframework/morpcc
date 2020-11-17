import morpfw
import rulez

from .modelui import ReferenceDataKeyCollectionUI, ReferenceDataKeyModelUI
from .schema import ReferenceDataKeySchema


class ReferenceDataKeyModel(morpfw.Model):
    schema = ReferenceDataKeySchema

    def ui(self):
        return ReferenceDataKeyModelUI(self.request, self, self.collection.ui())

    def export(self):
        result = {
            "name": self["name"],
            "description": self["description"],
            "values": {},
        }
        for v in self.referencedataproperties():
            result["values"][v["name"]] = v["value"]

        return result

    @morpfw.requestmemoize()
    def referencedataproperties(self):
        col = self.request.get_collection("morpcc.referencedataproperty")
        return col.search(rulez.field["referencedatakey_uuid"] == self.uuid)

    @morpfw.requestmemoize()
    def lookup_property(self, prop):
        col = self.request.get_collection("morpcc.referencedataproperty")
        res = col.search(
            rulez.and_(
                rulez.field["referencedatakey_uuid"] == self.uuid,
                rulez.field["name"] == prop,
            )
        )
        if res:
            return res[0]
        return None

    def before_delete(self):
        for p in self.referencedataproperties():
            p.delete()
        return super().before_delete()


class ReferenceDataKeyCollection(morpfw.Collection):
    schema = ReferenceDataKeySchema

    def ui(self):
        return ReferenceDataKeyCollectionUI(self.request, self)
