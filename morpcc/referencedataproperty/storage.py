import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ReferenceDataPropertyModel


class ReferenceDataProperty(morpfw.sql.Base):

    __tablename__ = "morpcc_referencedataproperty"

    name = sa.Column(sa.String(length=256), index=True)
    description = sa.Column(sa.Text())
    referencedatakey_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    value = sa.Column(sa.String(length=256))

    __table_args__ = (sa.UniqueConstraint("referencedatakey_uuid", "name", "deleted"),)


class ReferenceDataPropertyStorage(morpfw.SQLStorage):
    model = ReferenceDataPropertyModel
    orm_model = ReferenceDataProperty
