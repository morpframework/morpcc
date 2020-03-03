import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ReferenceEntity


class ReferenceData(morpfw.sql.Base):

    __tablename__ = "morpcc_referencedata"

    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    name = sa.Column(sa.String(length=1024), index=True)


class ReferenceDataStorage(morpfw.SQLStorage):
    model = ReferenceEntity
    orm_model = ReferenceData
