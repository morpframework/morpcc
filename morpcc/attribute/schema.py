import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpcc.deform.referencewidget import ReferenceWidget

ACCEPTED_TYPES = (
    ("string", "String"),
    ("integer", "Integer"),
    ("biginteger", "Big Integer"),
    ("float", "Float"),
    ("double", "Double"),
    ("date", "Date"),
    ("datetime", "DateTime"),
)


@dataclass
class AttributeSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None, metadata={"required": True, "editable": False}
    )
    type: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "deform.widget": SelectWidget(values=ACCEPTED_TYPES),
        },
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    required: typing.Optional[bool] = False
    datamodel_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "deform.widget": ReferenceWidget("morpcc.datamodel", "title", "uuid"),
        },
    )

    __unique_constraint__ = ["datamodel_uuid", "name"]
