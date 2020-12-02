import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import DictionaryElementValidatorAssignmentModel


class DictionaryElementValidatorAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_dictionaryelementvalidatorassignment"

    dictionaryelement_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    attributevalidator_name = sa.Column(sa.String(length=256), index=True)


class DictionaryElementValidatorAssignmentStorage(morpfw.SQLStorage):
    model = DictionaryElementValidatorAssignmentModel
    orm_model = DictionaryElementValidatorAssignment
