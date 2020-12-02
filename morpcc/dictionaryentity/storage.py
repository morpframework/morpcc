import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import DictionaryEntityModel


class DictionaryEntity(morpfw.sql.Base):

    __tablename__ = "morpcc_dictionaryentity"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    notes = sa.Column(sa.Text())


class DictionaryEntityStorage(morpfw.SQLStorage):
    model = DictionaryEntityModel
    orm_model = DictionaryEntity
