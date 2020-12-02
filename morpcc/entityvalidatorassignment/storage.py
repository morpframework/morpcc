import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EntityValidatorAssignmentModel


class EntityValidatorAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_entityvalidatorassignment"

    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    entityvalidator_name = sa.Column(sa.String(256), index=True)


class EntityValidatorAssignmentStorage(morpfw.SQLStorage):
    model = EntityValidatorAssignmentModel
    orm_model = EntityValidatorAssignment
