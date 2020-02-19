import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpcc.deform.referencewidget import ReferenceWidget


@dataclass
class ReferenceDataPropertySchema(morpfw.Schema):

    property: typing.Optional[str] = field(
        default=None,
        metadata={
            "deform.widget": SelectWidget(
                values=[("value", "Value"), ("label", "Label")]
            )
        },
    )
    value: typing.Optional[str] = None
    description: typing.Optional[str] = None
    referencedatakey_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "deform": {
                "widget": ReferenceWidget("morpcc.referencedatakey", "name", "uuid")
            }
        },
    )

    __unique_constraint__ = ["referencedatakey_uuid", "property"]
