import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator


@dataclass
class AttributeValidatorAssignmentSchema(morpfw.Schema):

    attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validator": [ReferenceValidator("morpcc.attribute", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.attribute", "title", "uuid"),
        },
    )
    attributevalidator_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validator": [ReferenceValidator("morpcc.attributevalidator", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.attributevalidator", "title", "uuid"
            ),
        },
    )
