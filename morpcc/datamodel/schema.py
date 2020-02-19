import typing
from dataclasses import dataclass, field

import morpfw
from morpcc.deform.referencewidget import ReferenceWidget
from morpfw.crud.field import Field


@dataclass
class DataModelSchema(morpfw.Schema):
    name: typing.Optional[str] = (
        Field().default(None).required().editable(False).init()
    )
    title: typing.Optional[str] = Field().default(None).required().init()
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})

    application_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "deform.widget": ReferenceWidget("morpcc.application", "title", "uuid"),
        },
    )
