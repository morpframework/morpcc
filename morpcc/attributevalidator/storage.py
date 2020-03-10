import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import AttributeValidatorModel


class AttributeValidator(morpfw.sql.Base):

    __tablename__ = "morpcc_attributevalidator"

    name = sa.Column(sa.String(length=1024), index=True)
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    type = sa.Column(sa.String(length=1024))
    notes = sa.Column(sa.Text())
    code = sa.Column(sa.Text())
    error_message = sa.Column(sa.String(length=1024))


class AttributeValidatorStorage(morpfw.SQLStorage):
    model = AttributeValidatorModel
    orm_model = AttributeValidator
