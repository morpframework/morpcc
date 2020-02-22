import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import SelectionAttributeModel


class SelectionAttribute(morpfw.sql.Base):

    __tablename__ = "morpcc_selectionattribute"

    name = sa.Column(sa.String(length=1024))
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    referencedata_name = sa.Column(sa.String(1024))
    referencedata_property = sa.Column(sa.String(length=1024))
    required = sa.Column(sa.Boolean())
    primary_key = sa.Column(sa.Boolean())
    entity_uuid = sa.Column(morpfw.sql.GUID())


class SelectionAttributeStorage(morpfw.SQLStorage):
    model = SelectionAttributeModel
    orm_model = SelectionAttribute
