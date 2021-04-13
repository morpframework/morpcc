import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ActivityLogModel


class ActivityLog(morpfw.sql.Base):

    __tablename__ = "morpcc_activitylog"

    userid = sa.Column(morpfw.sql.GUID())
    resource_uuid = sa.Column(morpfw.sql.GUID())
    metalink_type = sa.Column(sa.String(length=128))
    metalink = sa.Column(sajson.JSONField())
    view_name = sa.Column(sa.String(length=128))
    source_ip = sa.Column(sa.String(length=64))
    activity = sa.Column(sa.Text())
    request_url = sa.Column(sa.String(length=2000))
    request_method = sa.Column(sa.String(length=12))


class ActivityLogStorage(morpfw.SQLStorage):
    model = ActivityLogModel
    orm_model = ActivityLog
