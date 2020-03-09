import morpfw
import rulez

from ..referencedataproperty.path import get_collection as get_prop_collection
from .schema import ReferenceDataKeySchema


class ReferenceDataKeyModel(morpfw.Model):
    schema = ReferenceDataKeySchema

    def export(self):
        result = {
            "name": self["name"],
            "description": self["description"],
            "values": {},
        }
        for v in self.referencedatavalues():
            result["values"][v["name"]] = v["value"]

        return result

    def referencedatavalues(self):
        col = get_prop_collection(self.request)
        return col.search(rulez.field["referencedatakey_uuid"] == self.uuid)

    def before_delete(self):
        col = get_prop_collection(self.request)
        for v in col.search(rulez.field["referencedatakey_uuid"] == self.uuid):
            v.delete()


class ReferenceDataKeyCollection(morpfw.Collection):
    schema = ReferenceDataKeySchema
