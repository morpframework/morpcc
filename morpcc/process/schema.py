import typing
from dataclasses import dataclass, field
from datetime import datetime

import morpfw

from ..deform.codewidget import CodeWidget


@dataclass
class ProcessSchema(morpfw.Schema):

    signal: typing.Optional[str] = field(default=None, metadata={"required": True})
    task_id: typing.Optional[str] = field(
        default=None, metadata={"format": "uuid", "required": True}
    )
    start: typing.Optional[datetime] = None
    end: typing.Optional[datetime] = None
    params: typing.Optional[dict] = None
    traceback: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "text/python",
            "required": False,
            "deform.widget": CodeWidget(syntax="pytb"),
        },
    )

    __unique_constraint__ = ["task_id"]
