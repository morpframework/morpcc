import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from sqlalchemy import MetaData

from .model import EntityModel


class Entity(morpfw.sql.Base):

    __tablename__ = "morpcc_entity"

    name = sa.Column(sa.String(length=1024))
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())
    application_uuid = sa.Column(morpfw.sql.GUID())


class EntityStorage(morpfw.SQLStorage):
    model = EntityModel
    orm_model = Entity
