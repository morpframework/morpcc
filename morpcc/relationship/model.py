import morpfw
import rulez

from .modelui import RelationshipCollectionUI, RelationshipModelUI
from .schema import RelationshipSchema


class RelationshipModel(morpfw.Model):
    schema = RelationshipSchema

    def ui(self):
        return RelationshipModelUI(self.request, self, self.collection.ui())

    def reference_attribute(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.attribute", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        attr = col.get(self["reference_attribute_uuid"])
        return attr

    def reference_search_attribute(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.attribute", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        attr = col.get(self["reference_search_attribute_uuid"])
        return attr

    def datatype(self):
        refattr = self.reference_attribute()
        return refattr.datatype()

    def resolve_relationship(self, context):
        """ return the modelcontent of the relationship """
        attr = self.reference_attribute()
        col = attr.entity().content_collection()
        res = col.search(rulez.field[attr["name"]] == context[self["name"]])
        if res:
            return res[0]
        return None

    def entity(self):
        typeinfo = self.request.app.config.type_registry.get_typeinfo(
            name="morpcc.entity", request=self.request
        )

        col = typeinfo["collection_factory"](self.request)
        dm = col.get(self["entity_uuid"])
        return dm


class RelationshipCollection(morpfw.Collection):
    schema = RelationshipSchema

    def ui(self):
        return RelationshipCollectionUI(self.request, self)
