import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import Select2Widget, TextAreaWidget
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
class AttributeValidatorSchema(morpfw.Schema):

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
    type: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "searchable": True,
            "validators": [valid_type],
            "deform.widget": Select2Widget(
                values=[("", "")] + list(ACCEPTED_TYPES), placeholder=" "
            ),
        },
    )
    notes: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "text/html",
            "preparers": [HTMLSanitizer()],
            "deform.widget": RichTextWidget(),
        },
    )
    code: typing.Optional[str] = field(
        default="def validate(value):\n    return True",
        metadata={
            "format": "text/python",
            "required": True,
            "deform.widget": CodeWidget(),
        },
    )
    error_message: typing.Optional[str] = field(
        default=None, metadata={"required": True}
    )
