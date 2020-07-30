import morpfw
import rulez

from ..entitycontent.path import content_collection_factory
from .modelui import RelationshipCollectionUI, RelationshipModelUI
from .schema import RelationshipSchema


class RelationshipModel(morpfw.Model):
    schema = RelationshipSchema

    def ui(self):
        return RelationshipModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def reference_attribute(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.attribute", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        attr = col.get(self["reference_attribute_uuid"])
        return attr

    @morpfw.requestmemoize()
    def reference_search_attribute(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.attribute", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        attr = col.get(self["reference_search_attribute_uuid"])
        return attr

    @morpfw.requestmemoize()
    def datatype(self):
        refattr = self.reference_attribute()
        return refattr.datatype()

    @morpfw.requestmemoize()
    def entity(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.entity", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        dm = col.get(self["entity_uuid"])
        return dm

    @morpfw.requestmemoize()
    def reference_entity(self):
        return self.reference_attribute().entity()


class RelationshipCollection(morpfw.Collection):
    schema = RelationshipSchema

    def ui(self):
        return RelationshipCollectionUI(self.request, self)
