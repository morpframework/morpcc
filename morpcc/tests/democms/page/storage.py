import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import DataAssetModel


class DataAsset(morpfw.sql.Base):

    __tablename__ = 'dlcc_dataasset'

    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    location = sa.Column(sa.String(length=2048))


class DataAssetStorage(morpfw.SQLStorage):
    model = DataAssetModel
    orm_model = DataAsset
