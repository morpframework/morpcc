import morpfw
import rulez

from .modelui import SchemaCollectionUI, SchemaModelUI
from .schema import SchemaSchema


class SchemaModel(morpfw.Model):
    schema = SchemaSchema

    def ui(self):
        return SchemaModelUI(self.request, self, self.collection.ui())

    @morpfw.requestmemoize()
    def entities(self):
        col = self.request.get_collection("morpcc.entity")
        return col.search(rulez.field["schema_uuid"] == self.uuid)


class SchemaCollection(morpfw.Collection):
    schema = SchemaSchema

    def ui(self):
        return SchemaCollectionUI(self.request, self)
