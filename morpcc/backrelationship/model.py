import typing

import morpfw
import rulez

from .modelui import BackRelationshipCollectionUI, BackRelationshipModelUI
from .schema import BackRelationshipSchema


class BackRelationshipModel(morpfw.Model):
    schema = BackRelationshipSchema

    def ui(self):
        return BackRelationshipModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def datatype(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.attribute", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        attr = col.get(self["reference_attribute_uuid"])
        return typing.List[attr.entity().dataclass()]

    @morpfw.requestmemoize()
    def reference_relationship(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.relationship", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        rel = col.get(self["reference_relationship_uuid"])
        return rel

    @morpfw.requestmemoize()
    def reference_entity(self):
        rel = self.reference_relationship()
        return rel.entity()


class BackRelationshipCollection(morpfw.Collection):
    schema = BackRelationshipSchema

    def ui(self):
        return BackRelationshipCollectionUI(self.request, self)
