import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ReferenceDataModel


class ReferenceData(morpfw.sql.Base):

    __tablename__ = "morpcc_referencedata"

    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    name = sa.Column(sa.String(length=256), index=True)


class ReferenceDataStorage(morpfw.SQLStorage):
    model = ReferenceDataModel
    orm_model = ReferenceData
