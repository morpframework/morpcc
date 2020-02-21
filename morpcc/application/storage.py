import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ApplicationModel, BehaviorableApplicationModel


class Application(morpfw.sql.Base):

    __tablename__ = "morpcc_application"

    name = sa.Column(sa.String(length=1024))
    title = sa.Column(sa.String(length=1024))
    description = sa.Column(sa.Text())


class ApplicationStorage(morpfw.SQLStorage):
    model = BehaviorableApplicationModel
    orm_model = Application
