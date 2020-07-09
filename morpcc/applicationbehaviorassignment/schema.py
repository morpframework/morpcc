import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class ApplicationBehaviorAssignmentSchema(morpfw.Schema):

    behavior: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [VocabularyValidator("morpcc.application_behaviors")],
            "deform.widget": VocabularyWidget("morpcc.application_behaviors"),
        },
    )
    application_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Application",
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.application", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.application", "title", "uuid"),
        },
    )
