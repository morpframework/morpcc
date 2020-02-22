import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import TextAreaWidget

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class AttributeConstraintSchema(morpfw.Schema):

    title: typing.Optional[str] = None
    validator: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [VocabularyValidator("morpcc.attributevalidators")],
            "deform.widget": VocabularyWidget("morpcc.attributevalidators"),
        },
    )
    parameters: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "format": "uuid",
            "validators": [ReferenceValidator("morpcc.attribute", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.attribute", "title", "uuid"),
        },
    )
