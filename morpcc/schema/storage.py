import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import SchemaModel


class Schema(morpfw.sql.Base):

    __tablename__ = "morpcc_schema"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())

    __table_args__ = (sa.UniqueConstraint("name", "deleted"),)


class SchemaStorage(morpfw.SQLStorage):
    model = SchemaModel
    orm_model = Schema
