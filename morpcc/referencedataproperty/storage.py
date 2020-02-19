import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import ReferenceDataPropertyModel


class ReferenceDataProperty(morpfw.sql.Base):

    __tablename__ = "morpcc_referencedataproperty"

    description = sa.Column(sa.Text())
    referencedatakey_uuid = sa.Column(morpfw.sql.GUID())
    property = sa.Column(sa.String())
    value = sa.Column(sa.String())

    __table_args__ = (sa.UniqueConstraint("referencedatakey_uuid", "property"),)


class ReferenceDataPropertyStorage(morpfw.SQLStorage):
    model = ReferenceDataPropertyModel
    orm_model = ReferenceDataProperty

