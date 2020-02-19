import typing
from dataclasses import dataclass, field

import morpfw


@dataclass
class ReferenceDataSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None, metadata={"required": True, "editable": False}
    )
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None

    __unique_constraint__ = ["name"]
