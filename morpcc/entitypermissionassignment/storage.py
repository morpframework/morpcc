import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EntityPermissionAssignmentModel


class EntityPermissionAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_entitypermissionassignment"

    application_uuid = sa.Column(morpfw.sql.GUID())
    entity_uuid = sa.Column(morpfw.sql.GUID())
    permission = sa.Column(sa.String(length=256))
    roles = sa.Column(sajson.JSONField())
    rule = sa.Column(sa.String(length=24))
    enabled = sa.Column(sa.Boolean())


class EntityPermissionAssignmentStorage(morpfw.SQLStorage):
    model = EntityPermissionAssignmentModel
    orm_model = EntityPermissionAssignment
