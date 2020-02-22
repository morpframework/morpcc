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
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None

    __unique_constraint__ = ["name"]
