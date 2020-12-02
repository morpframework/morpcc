import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EntityValidatorModel


class EntityValidator(morpfw.sql.Base):

    __tablename__ = "morpcc_entityvalidator"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    notes = sa.Column(sa.Text())
    code = sa.Column(sa.Text())
    error_message = sa.Column(sa.String(length=1024))


class EntityValidatorStorage(morpfw.SQLStorage):
    model = EntityValidatorModel
    orm_model = EntityValidator
