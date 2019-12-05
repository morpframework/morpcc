import morpfw
from .schema import SettingSchema


class SettingModel(morpfw.Model):
    schema = SettingSchema


class SettingCollection(morpfw.Collection):
    schema = SettingSchema
