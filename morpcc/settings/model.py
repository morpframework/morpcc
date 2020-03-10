import morpfw

from .modelui import SettingCollectionUI, SettingModelUI
from .schema import SettingSchema


class SettingModel(morpfw.Model):
    schema = SettingSchema

    def ui(self):
        return SettingModelUI(self.request, self, self.collection.ui())


class SettingCollection(morpfw.Collection):
    schema = SettingSchema

    def ui(self):
        return SettingCollectionUI(self.request, self)
