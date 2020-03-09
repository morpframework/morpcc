import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import AttributeValidatorModel


class AttributeValidator(morpfw.sql.Base):

    __tablename__ = "morpcc_attributevalidator"

    title = sa.Column(sa.String(length=1024))
    validator = sa.Column(sa.String(length=1024))
    parameters = sa.Column(sa.Text())
    attribute_uuid = sa.Column(morpfw.sql.GUID(), index=True)


class AttributeValidatorStorage(morpfw.SQLStorage):
    model = AttributeValidatorModel
    orm_model = AttributeValidator
