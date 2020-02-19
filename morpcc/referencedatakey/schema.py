import typing
from dataclasses import dataclass, field

import morpfw
from morpcc.deform.referencewidget import ReferenceWidget


@dataclass
class ReferenceDataKeySchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "editable": False,
            "required": True
        }
    )
    description: typing.Optional[str] = None
    referencedata_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "editable": False,
            "required": True,
            "deform.widget": ReferenceWidget("morpcc.referencedata", "title", "uuid")
        },
    )

    __unique_constraint__ = ["name", "referencedata_uuid"]
