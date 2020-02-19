import typing

import morpfw
import rulez

from .modelui import BackRelationshipCollectionUI, BackRelationshipModelUI
from .schema import BackRelationshipSchema


class BackRelationshipModel(morpfw.Model):
    schema = BackRelationshipSchema

    def ui(self):
        return BackRelationshipModelUI(self.request, self, self.collection.ui())

    def datatype(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.attribute", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        attr = col.get(self["reference_attribute_uuid"])
        return typing.List[attr.datamodel().dataclass()]

    def reference_relationship(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.relationship", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        rel = col.get(self["reference_relationship_uuid"])
        return rel

    def content_collection(self):
        rel = self.reference_relationship()
        dm = rel.datamodel()
        return dm.content_collection()

    def resolve_relationship(self, context):
        rel = self.reference_relationship()
        dm = rel.datamodel()
        col = dm.content_collection()

        attr = rel.reference_attribute()

        result = col.search(rulez.field[rel["name"]] == context[attr["name"]])
        return result


class BackRelationshipCollection(morpfw.Collection):
    schema = BackRelationshipSchema

    def ui(self):
        return BackRelationshipCollectionUI(self.request, self)
