import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EntityConstraintModel


class EntityConstraint(morpfw.sql.Base):

    __tablename__ = "morpcc_entityconstraint"

    title = sa.Column(sa.String(length=1024))
    validator = sa.Column(sa.String(length=1024))
    parameters = sa.Column(sa.Text())
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)


class EntityConstraintStorage(morpfw.SQLStorage):
    model = EntityConstraintModel
    orm_model = EntityConstraint
