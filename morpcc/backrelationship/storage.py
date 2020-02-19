import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import BackRelationshipModel


class BackRelationship(morpfw.sql.Base):

    __tablename__ = "morpcc_backrelationship"

    name = sa.Column(sa.String(length=1024))
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    datamodel_uuid = sa.Column(morpfw.sql.GUID)
    reference_relationship_uuid = sa.Column(morpfw.sql.GUID)


class BackRelationshipStorage(morpfw.SQLStorage):
    model = BackRelationshipModel
    orm_model = BackRelationship
