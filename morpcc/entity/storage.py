import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from sqlalchemy import MetaData

from .model import EntityModel


class Entity(morpfw.sql.Base):

    __tablename__ = "morpcc_entity"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    icon = sa.Column(sa.String(length=64))

    allow_invalid = sa.Column(sa.Boolean())
    schema_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    is_primary = sa.Column(sa.Boolean(), index=True)


class EntityStorage(morpfw.SQLStorage):
    model = EntityModel
    orm_model = Entity
