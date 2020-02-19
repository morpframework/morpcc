import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import AttributeConstraintModel


class AttributeConstraint(morpfw.sql.Base):

    __tablename__ = "morpcc_attributeconstraint"

    title = sa.Column(sa.String(length=1024))
    validator = sa.Column(sa.String(length=1024))
    parameters = sa.Column(sa.Text())
    attribute_uuid = sa.Column(morpfw.sql.GUID())


class AttributeConstraintStorage(morpfw.SQLStorage):
    model = AttributeConstraintModel
    orm_model = AttributeConstraint
