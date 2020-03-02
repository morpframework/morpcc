import typing
from dataclasses import dataclass, field

import morpfw
from morpfw.validator.field import valid_identifier

from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator
from ..validator.field import valid_refdatakey


@dataclass
class ReferenceDataKeySchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "editable": False,
            "validators": [valid_refdatakey],
            "required": True,
        },
    )
    description: typing.Optional[str] = None
    referencedata_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "editable": False,
            "required": True,
            "validators": [ReferenceValidator("morpcc.referencedata", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.referencedata", "title", "uuid"),
        },
    )

    __unique_constraint__ = ["name", "referencedata_uuid"]
