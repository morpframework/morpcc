import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EndpointModel


class Endpoint(morpfw.sql.Base):

    __tablename__ = "morpcc_endpoint"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    notes = sa.Column(sa.Text())


class EndpointStorage(morpfw.SQLStorage):
    model = EndpointModel
    orm_model = Endpoint
