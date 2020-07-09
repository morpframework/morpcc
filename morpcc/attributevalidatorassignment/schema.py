import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator
from .form_validator import valid_assignment


@dataclass
class AttributeValidatorAssignmentSchema(morpfw.Schema):

    attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Attribute",
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.attribute", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.attribute", "title", "uuid"),
        },
    )
    attributevalidator_name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [ReferenceValidator("morpcc.attributevalidator", "name")],
            "deform.widget": ReferenceWidget(
                "morpcc.attributevalidator", "title", "name"
            ),
        },
    )

    __validators__ = [valid_assignment]
