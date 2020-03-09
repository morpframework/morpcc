import typing
from dataclasses import dataclass, field

import morpfw
from morpfw.validator.field import valid_identifier


@dataclass
class ReferenceDataSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [valid_identifier],
            "editable": False,
        },
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})

    __unique_constraint__ = ["name"]
