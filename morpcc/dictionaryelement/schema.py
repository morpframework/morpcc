import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpfw.validator.field import valid_identifier

from ..attribute.schema import ACCEPTED_TYPES, valid_type
from ..deform.referencewidget import ReferenceWidget
from ..deform.richtextwidget import RichTextWidget
from ..preparer.html import HTMLSanitizer
from ..referencedataproperty.schema import PROPERTY_TYPES, valid_property_types
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator
from .form_validator import valid_refdata


@dataclass
class DictionaryElementSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None, metadata={"required": True, "validators": [valid_identifier]}
    )
    dictionaryentity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Dictionary Entity",
            "format": "uuid",
            "validators": [ReferenceValidator("morpcc.dictionaryentity", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.dictionaryentity", "title", "uuid"
            ),
        },
    )
    type: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [valid_type],
            "deform.widget": SelectWidget(values=ACCEPTED_TYPES),
        },
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    notes: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "text",
            "preparers": [HTMLSanitizer()],
            "deform.widget": RichTextWidget(),
        },
    )
    referencedata_name: typing.Optional[str] = field(
        default=None,
        metadata={
            "validators": [ReferenceValidator("morpcc.referencedata", "name")],
            "deform.widget": ReferenceWidget("morpcc.referencedata", "title", "name"),
        },
    )
    referencedata_property: typing.Optional[str] = field(
        default=None,
        metadata={
            "validators": [valid_property_types],
            "deform.widget": SelectWidget(values=PROPERTY_TYPES),
        },
    )

    __unique_constraint__ = ["name"]

    __validators__ = [valid_refdata]
