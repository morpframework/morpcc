import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.codewidget import JSONCodeWidget
from ..deform.referencewidget import ReferenceWidget


@dataclass
class ActivityLogSchema(morpfw.Schema):

    userid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "deform.widget": ReferenceWidget(
                "morpfw.pas.user", term_field="username", value_field="uuid"
            ),
        },
    )
    source_ip: typing.Optional[str] = None
    resource_uuid: typing.Optional[str] = None
    metalink_type: typing.Optional[str] = None
    metalink: typing.Optional[dict] = field(
        default=None, metadata={"deform.widget": JSONCodeWidget()}
    )
    view_name: typing.Optional[str] = None
    activity: typing.Optional[str] = None
    request_url: typing.Optional[str] = None
    request_method: typing.Optional[str] = None
