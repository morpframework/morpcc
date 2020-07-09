import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget

from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator

PROPERTY_TYPES = [("label", "Label"), ("description", "Description")]


def valid_property_types(request, schema, field, value, mode=None):
    if value not in [k for k, v in PROPERTY_TYPES]:
        return "Invalid property type {}".format(value)


@dataclass
class ReferenceDataPropertySchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [valid_property_types],
            "deform.widget": SelectWidget(values=PROPERTY_TYPES),
        },
    )
    value: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    referencedatakey_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Reference Data Key",
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.referencedatakey", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.referencedatakey", "name", "uuid"),
        },
    )

    __unique_constraint__ = ["referencedatakey_uuid", "name"]
