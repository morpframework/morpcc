import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import DictionaryElementModel


class DictionaryElement(morpfw.sql.Base):

    __tablename__ = "morpcc_dictionaryelement"

    dictionaryentity_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    name = sa.Column(sa.String(length=256), index=True)
    type = sa.Column(sa.String(length=256))
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    notes = sa.Column(sa.Text())
    referencedata_name = sa.Column(sa.String(length=256))
    referencedata_property = sa.Column(sa.String(length=256))


class DictionaryElementStorage(morpfw.SQLStorage):
    model = DictionaryElementModel
    orm_model = DictionaryElement
