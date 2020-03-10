import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator
from .form_validator import valid_assignment


@dataclass
class DictionaryElementValidatorAssignmentSchema(morpfw.Schema):

    dictionaryelement_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.dictionaryelement", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.dictionaryelement", "title", "uuid"
            ),
        },
    )
    attributevalidator_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.attributevalidator", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.attributevalidator", "title", "uuid"
            ),
        },
    )

    __validators__ = [valid_assignment]
