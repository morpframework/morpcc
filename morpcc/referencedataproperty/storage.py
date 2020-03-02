import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ReferenceDataPropertyModel


class ReferenceDataProperty(morpfw.sql.Base):

    __tablename__ = "morpcc_referencedataproperty"

    name = sa.Column(sa.String())
    description = sa.Column(sa.Text())
    referencedatakey_uuid = sa.Column(morpfw.sql.GUID())
    value = sa.Column(sa.String())

    __table_args__ = (sa.UniqueConstraint("referencedatakey_uuid", "name"),)


class ReferenceDataPropertyStorage(morpfw.SQLStorage):
    model = ReferenceDataPropertyModel
    orm_model = ReferenceDataProperty
