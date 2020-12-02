import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import BackRelationshipModel


class BackRelationship(morpfw.sql.Base):

    __tablename__ = "morpcc_backrelationship"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    reference_relationship_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    single_relation = sa.Column(sa.Boolean())


class BackRelationshipStorage(morpfw.SQLStorage):
    model = BackRelationshipModel
    orm_model = BackRelationship
