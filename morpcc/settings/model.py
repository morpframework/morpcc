import dataclasses

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
        return self.create({"key": key, "data": {"value": None}})

    def resolve_raw(self, key, default=_marker):
        """ return raw serialized settings value """
        item = self.get_by_key(key)
        if default is not _marker:
            return item["data"].get("value", default)
        return item["data"].get("value")

    def resolve(self, key, default=_marker):
        """ return deserialized settings value """
        item = self.get_by_key(key)
        pages = self.request.app.config.setting_page_registry.values(self.request)
        for p in pages:
            schema = p.factory(self.request)
            for fname, field in schema.__dataclass_fields__.items():
                if field.metadata.get("morpcc.setting.key", None) == key:
                    fschema = p.jsonformschema(self, self.request)
                    serde = fschema[fname]
                    value = item["data"]["value"]
                    if value is None:
                        if not isinstance(field.default, dataclasses._MISSING_TYPE):
                            value = field.default
                        elif not isinstance(
                            field.default_factory, dataclasses._MISSING_TYPE
                        ):
                            value = field.default_factory()
                    else:
                        value = serde.deserialize(value)
                    return value
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
