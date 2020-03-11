import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import EndpointHandlerModel


class EndpointHandler(morpfw.sql.Base):

    __tablename__ = "morpcc_endpointhandler"

    endpoint_uuid = sa.Column(morpfw.sql.GUID())
    method = sa.Column(sa.String(length=20))
    code = sa.Column(sa.Text())


class EndpointHandlerStorage(morpfw.SQLStorage):
    model = EndpointHandlerModel
    orm_model = EndpointHandler
