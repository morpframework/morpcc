import morpfw
import rulez

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

    def get_by_key(self, key):
        items = self.search(rulez.field["key"] == key)
        if items:
            return items[0]
        return self.create({"key": key, "value": None})
