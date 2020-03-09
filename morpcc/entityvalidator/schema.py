#
import typing
from dataclasses import dataclass, field

import morpfw

#
from deform.widget import TextAreaWidget

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class EntityValidatorSchema(morpfw.Schema):

    title: typing.Optional[str] = None
    validator: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [VocabularyValidator("morpcc.entityvalidators")],
            "deform.widget": VocabularyWidget("morpcc.entityvalidators"),
        },
    )
    parameters: typing.Optional[str] = field(
        default=None, metadata={"deform.widget": TextAreaWidget()}
    )
    entity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "validators": [ReferenceValidator("morpcc.entity", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.entity", "title", "uuid"),
        },
    )
