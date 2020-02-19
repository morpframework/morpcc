import typing
from dataclasses import dataclass, field

import morpfw
from morpcc.deform.referencewidget import ReferenceWidget


@dataclass
class ReferenceDataKeySchema(morpfw.Schema):

    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    referencedata_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "deform.widget": ReferenceWidget("morpcc.referencedata", "title", "uuid")
        },
    )

    __unique_constraint__ = ["name", "referencedata_uuid"]
