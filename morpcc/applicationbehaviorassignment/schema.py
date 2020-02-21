import typing
from dataclasses import dataclass, field

import morpfw
from morpcc.deform.referencewidget import ReferenceWidget
from morpcc.deform.vocabularywidget import VocabularyWidget


@dataclass
class ApplicationBehaviorAssignmentSchema(morpfw.Schema):

    behavior: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "deform.widget": VocabularyWidget("morpcc.application_behaviors"),
        },
    )
    application_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "deform.widget": ReferenceWidget("morpcc.application", "title", "uuid"),
        },
    )
