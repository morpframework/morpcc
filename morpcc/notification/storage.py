import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import NotificationModel


class Notification(morpfw.sql.Base):

    __tablename__ = 'morpcc_notification'

    message = sa.Column(sa.Text())
    userid = sa.Column(morpfw.sql.GUID)
    read = sa.Column(sa.DateTime)


class NotificationStorage(morpfw.SQLStorage):
    model = NotificationModel
    orm_model = Notification
