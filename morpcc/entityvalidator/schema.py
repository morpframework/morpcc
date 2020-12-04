#
import typing
from dataclasses import dataclass, field

import morpfw

#
from deform.widget import SelectWidget, TextAreaWidget
from morpfw.validator.field import valid_namespaced_identifier

from ..attribute.schema import ACCEPTED_TYPES, valid_type
from ..deform.codewidget import CodeWidget
from ..deform.referencewidget import ReferenceWidget
from ..deform.richtextwidget import RichTextWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..preparer.html import HTMLSanitizer
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


@dataclass
class EntityValidatorSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "searchable": True,
            "validators": [valid_namespaced_identifier],
        },
    )

    title: typing.Optional[str] = field(
        default=None, metadata={"required": True, "searchable": True}
    )
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    notes: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "text/html",
            "preparers": [HTMLSanitizer()],
            "deform.widget": RichTextWidget(),
        },
    )
    code: typing.Optional[str] = field(
        default="def validate(data):\n    return True",
        metadata={
            "format": "text/python",
            "required": True,
            "deform.widget": CodeWidget(),
        },
    )
    error_message: typing.Optional[str] = field(
        default=None, metadata={"required": True}
    )

    __references__ = [
        morpfw.BackReference(
            "assignments", "morpcc.entityvalidatorassignment", "entityvalidator_name"
        )
    ]
