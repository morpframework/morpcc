import typing
from dataclasses import dataclass, field
from datetime import datetime

import morpfw
from morpcc.deform.referencewidget import UserReferenceWidget


@dataclass
class NotificationSchema(morpfw.Schema):

    message: typing.Optional[str] = None
    userid: typing.Optional[str] = field(
        default=None,
        metadata={"format": "uuid", "deform.widget": UserReferenceWidget()},
    )
    read: typing.Optional[datetime] = None
