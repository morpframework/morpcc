import morpfw
import rulez

from .modelui import SettingCollectionUI, SettingModelUI
from .schema import SettingSchema

_marker = object()


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

    def resolve(self, key, default=_marker):
        item = self.get_by_key(key)
        pages = self.request.app.config.setting_page_registry.values(self.request)
        for p in pages:
            schema = p.factory(self.request)
            for fname, field in schema.__dataclass_fields__.items():
                if field.metadata.get("morpcc.setting.key", None) == key:
                    fschema = p.jsonformschema(self, self.request)
                    serde = fschema[fname]
                    return serde.deserialize(item["data"]["value"])
        if default is _marker:
            raise KeyError(key)
        return default

    def store(self, key, value):
        item = self.get_by_key(key)
        pages = self.request.app.config.setting_page_registry.values(self.request)
        for p in pages:
            schema = p.factory(self.request)
            for fname, field in schema.__dataclass_fields__.items():
                if field.metadata.get("morpcc.setting.key", None) == key:
                    fschema = p.jsonformschema(self, self.request)
                    serde = fschema[fname]
                    value = serde.serialize(value)
                    item.update({"data": {"value": value}})
                    return
        raise KeyError(key)
