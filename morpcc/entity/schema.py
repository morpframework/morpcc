import typing
from dataclasses import dataclass, field

import morpfw
from morpfw.crud.field import Field
from morpfw.validator.field import valid_identifier

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class EntitySchema(morpfw.Schema):
    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "validators": [valid_identifier],
        },
    )
    title: typing.Optional[str] = Field().default(None).required().init()
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    icon: typing.Optional[str] = field(
        default=None,
        metadata={
            "validators": [VocabularyValidator("morpcc.fa-icons")],
            "deform.widget": VocabularyWidget("morpcc.fa-icons"),
        },
    )

    application_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.application", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.application", "title", "uuid"),
        },
    )

    __unique_constraint__ = ["application_uuid", "name"]
