import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import RelationshipModel


class Relationship(morpfw.sql.Base):

    __tablename__ = "morpcc_relationship"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    reference_attribute_uuid = sa.Column(morpfw.sql.GUID())
    reference_search_attribute_uuid = sa.Column(morpfw.sql.GUID())
    required = sa.Column(sa.Boolean())
    primary_key = sa.Column(sa.Boolean())


class RelationshipStorage(morpfw.SQLStorage):
    model = RelationshipModel
    orm_model = Relationship
