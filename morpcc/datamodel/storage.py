import sqlalchemy as sa
from sqlalchemy import MetaData

import morpfw
import morpfw.sql
import sqlalchemy_jsonfield as sajson

from .model import DataModelModel


class DataModel(morpfw.sql.Base):

    __tablename__ = "morpcc_datamodel"

    name = sa.Column(sa.String(length=1024))
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    application_uuid = sa.Column(morpfw.sql.GUID())


class DataModelStorage(morpfw.SQLStorage):
    model = DataModelModel
    orm_model = DataModel
