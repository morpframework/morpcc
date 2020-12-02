import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ReferenceDataKeyModel


class ReferenceDataKey(morpfw.sql.Base):

    __tablename__ = "morpcc_referencedatakey"

    name = sa.Column(sa.String(length=256), index=True)
    description = sa.Column(sa.Text())
    referencedata_uuid = sa.Column(morpfw.sql.GUID)

    __table_args__ = (sa.UniqueConstraint("referencedata_uuid", "name", "deleted"),)


class ReferenceDataKeyStorage(morpfw.SQLStorage):
    model = ReferenceDataKeyModel
    orm_model = ReferenceDataKey
