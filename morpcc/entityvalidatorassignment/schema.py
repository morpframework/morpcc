import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator


@dataclass
class EntityValidatorAssignmentSchema(morpfw.Schema):

    entity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.entity", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.entity", "title", "uuid"),
        },
    )
    entityvalidator_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.entityvalidator", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.entityvalidator", "title", "uuid"),
        },
    )
