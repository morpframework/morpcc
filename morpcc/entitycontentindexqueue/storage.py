import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson
from .model import EntityContentIndexQueueModel


class EntityContentIndexQueue(morpfw.sql.Base):

    __tablename__ = 'morpcc_entitycontentindexqueue'

    application_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    entity_uuid = sa.Column(morpfw.sql.GUID(), index=True)
    record_uuid = sa.Column(morpfw.sql.GUID())
    action = sa.Column(sa.String(128), index=True)

    __table_args__ = (
        sa.Index(
            "entitycontentindexqueue_entity_index",
            "application_uuid",
            "entity_uuid",
        ),
    )

class EntityContentIndexQueueStorage(morpfw.SQLStorage):
    model = EntityContentIndexQueueModel
    orm_model = EntityContentIndexQueue
