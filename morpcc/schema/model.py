import morpfw

from .modelui import SchemaCollectionUI, SchemaModelUI
from .schema import SchemaSchema


class SchemaModel(morpfw.Model):
    schema = SchemaSchema

    def ui(self):
        return SchemaModelUI(self.request, self, self.collection.ui())


class SchemaCollection(morpfw.Collection):
    schema = SchemaSchema

    def ui(self):
        return SchemaCollectionUI(self.request, self)
