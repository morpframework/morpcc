import morpfw

from .modelui import ReferenceDataPropertyCollectionUI, ReferenceDataPropertyModelUI
from .schema import ReferenceDataPropertySchema


class ReferenceDataPropertyModel(morpfw.Model):
    schema = ReferenceDataPropertySchema

    def ui(self):
        return ReferenceDataPropertyModelUI(self.request, self, self.collection.ui())


class ReferenceDataPropertyCollection(morpfw.Collection):
    schema = ReferenceDataPropertySchema

    def ui(self):
        return ReferenceDataPropertyCollectionUI(self.request, self)
