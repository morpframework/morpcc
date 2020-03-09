import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EntityValidatorModel


class EntityValidator(morpfw.sql.Base):

    __tablename__ = "morpcc_entityvalidator"

    title = sa.Column(sa.String(length=1024))
    validator = sa.Column(sa.String(length=1024))
    parameters = sa.Column(sa.Text())
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)


class EntityValidatorStorage(morpfw.SQLStorage):
    model = EntityValidatorModel
    orm_model = EntityValidator
