import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ApplicationBehaviorAssignmentModel


class ApplicationBehaviorAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_applicationbehaviorassignment"

    behavior = sa.Column(sa.String(length=256))
    application_uuid = sa.Column(morpfw.sql.GUID(), index=True)


class ApplicationBehaviorAssignmentStorage(morpfw.SQLStorage):
    model = ApplicationBehaviorAssignmentModel
    orm_model = ApplicationBehaviorAssignment
