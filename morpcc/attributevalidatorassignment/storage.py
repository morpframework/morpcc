import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import AttributeValidatorAssignmentModel


class AttributeValidatorAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_attributevalidatorassignment"

    attribute_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    attributevalidator_name = sa.Column(sa.String(length=256), index=True)


class AttributeValidatorAssignmentStorage(morpfw.SQLStorage):
    model = AttributeValidatorAssignmentModel
    orm_model = AttributeValidatorAssignment
