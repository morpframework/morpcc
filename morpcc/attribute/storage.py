import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import AttributeModel


class Attribute(morpfw.sql.Base):

    __tablename__ = "morpcc_attribute"

    name = sa.Column(sa.String(length=1024), index=True)
    type = sa.Column(sa.String(length=1024))
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    required = sa.Column(sa.Boolean())
    primary_key = sa.Column(sa.Boolean())
    default_factory = sa.Column(sa.String())
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    dictionaryelement_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    allow_invalid = sa.Column(sa.Boolean())
    searchable = sa.Column(sa.Boolean())
    schemata = sa.Column(sa.String())
    order = sa.Column(sa.Integer())


class AttributeStorage(morpfw.SQLStorage):
    model = AttributeModel
    orm_model = Attribute
