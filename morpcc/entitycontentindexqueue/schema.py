import typing
from dataclasses import dataclass, field

import deform.widget
import morpfw

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class EntityContentIndexQueueSchema(morpfw.Schema):

    application_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Application UUID",
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.application", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.application", "title", "uuid"),
        },
    )

    entity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Entity UUID",
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.entity", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.entity", "title", "uuid"),
        },
    )

    record_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Record UUID",
            "format": "uuid",
            "required": True,
            "editable": False,
        },
    )

    action: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Action",
            "required": True,
            "editable": False,
            "deform.widget": deform.widget.SelectWidget(
                values=[("index", "Index"), ("unindex", "Unindex")]
            ),
        },
    )
