import morpfw
from .schema import ReferenceDataKeySchema
from ..referencedataproperty.path import get_collection as get_prop_collection
import rulez


class ReferenceDataKeyModel(morpfw.Model):
    schema = ReferenceDataKeySchema

    def referencedatavalues(self):
        col = get_prop_collection(self.request)
        return col.search(rulez.field["referencedatakey_uuid"] == self.uuid)

    def before_delete(self):
        col = get_prop_collection(self.request)
        for v in col.search(rulez.field["referencedatakey_uuid"] == self.uuid):
            v.delete()


class ReferenceDataKeyCollection(morpfw.Collection):
    schema = ReferenceDataKeySchema

