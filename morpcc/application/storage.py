import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ApplicationModel, BehaviorableApplicationModel


class Application(morpfw.sql.Base):

    __tablename__ = "morpcc_application"

    name = sa.Column(sa.String(length=256), index=True)
    title = sa.Column(sa.String(length=256))
    description = sa.Column(sa.Text())
    icon = sa.Column(sa.String(length=64))
    schema_uuid = sa.Column(morpfw.sql.GUID())


class ApplicationStorage(morpfw.SQLStorage):
    model = BehaviorableApplicationModel
    orm_model = Application
