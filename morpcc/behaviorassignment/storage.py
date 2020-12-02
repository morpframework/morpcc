import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import BehaviorAssignmentModel


class BehaviorAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_behaviorassignment"

    behavior = sa.Column(sa.String(length=256))
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)


class BehaviorAssignmentStorage(morpfw.SQLStorage):
    model = BehaviorAssignmentModel
    orm_model = BehaviorAssignment
