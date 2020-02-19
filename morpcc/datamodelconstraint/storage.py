import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import DataModelConstraintModel


class DataModelConstraint(morpfw.sql.Base):

    __tablename__ = "morpcc_datamodelconstraint"

    title = sa.Column(sa.String(length=1024))
    validator = sa.Column(sa.String(length=1024))
    parameters = sa.Column(sa.Text())
    datamodel_uuid = sa.Column(morpfw.sql.GUID())


class DataModelConstraintStorage(morpfw.SQLStorage):
    model = DataModelConstraintModel
    orm_model = DataModelConstraint
