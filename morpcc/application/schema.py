#
import typing
from dataclasses import dataclass, field

import morpfw

#
from deform.widget import TextAreaWidget
from morpfw.validator.field import valid_identifier

from ..deform.vocabularywidget import VocabularyWidget


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
        default=None, metadata={"deform.widget": VocabularyWidget("morpcc.fa-icons")}
    )

    __unique_constraint__ = ["name"]
