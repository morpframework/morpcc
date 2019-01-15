import morpfw
from .schema import DataAssetSchema


class DataAssetModel(morpfw.Model):
    schema = DataAssetSchema


class DataAssetCollection(morpfw.Collection):
    schema = DataAssetSchema
