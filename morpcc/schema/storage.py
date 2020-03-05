import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import SchemaModel


class Schema(morpfw.sql.Base):

    __tablename__ = "morpcc_schema"

    name = sa.Column(sa.String(length=1024), unique=True)
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())


class SchemaStorage(morpfw.SQLStorage):
    model = SchemaModel
    orm_model = Schema
