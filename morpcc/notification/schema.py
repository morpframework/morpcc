import morpfw
from dataclasses import dataclass, field
import typing
from datetime import datetime
from morpcc.deform.referencewidget import UserReferenceWidget


@dataclass
class NotificationSchema(morpfw.Schema):

    message: typing.Optional[str] = None
    userid: typing.Optional[str] = field(
        default=None,
        metadata={
            'deform': {
                'widget': UserReferenceWidget()
            }
        }
    )
    read: typing.Optional[datetime] = None
