#
import typing
from dataclasses import dataclass, field

import morpfw

#
from deform.widget import TextAreaWidget
from morpfw.validator.field import valid_identifier

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class ApplicationSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "validators": [valid_identifier],
        },
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})

    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    icon: typing.Optional[str] = field(
        default=None,
        metadata={
            "validators": [VocabularyValidator("morpcc.fa-icons")],
            "deform.widget": VocabularyWidget("morpcc.fa-icons"),
        },
    )
    schema_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Schema",
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.schema", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.schema", "title", "uuid"),
        },
    )

    __unique_constraint__ = ["name"]
    __references__ = [morpfw.Reference("schema_uuid", "morpcc.schema")]
