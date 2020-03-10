import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpfw.validator.field import valid_identifier

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator
from .form_validator import (
    required_if_primary_key,
    unique_attribute,
    valid_dictionary_element,
)

ACCEPTED_TYPES = (
    ("string", "String"),
    ("text", "Text"),
    ("richtext", "Rich Text"),
    ("integer", "Integer"),
    ("biginteger", "Big Integer"),
    ("float", "Float"),
    ("double", "Double"),
    ("date", "Date"),
    ("datetime", "DateTime"),
)


def valid_type(request, schema, field, value, mode=None):
    if value not in [k for k, v in ACCEPTED_TYPES]:
        return "Invalid type"


@dataclass
class AttributeSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "validators": [valid_identifier],
        },
    )
    type: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "validators": [valid_type],
            "deform.widget": SelectWidget(values=ACCEPTED_TYPES),
        },
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    required: typing.Optional[bool] = False
    primary_key: typing.Optional[bool] = False
    default_factory: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": False,
            "validators": [VocabularyValidator("morpcc.default_factories")],
            "deform.widget": VocabularyWidget("morpcc.default_factories"),
        },
    )
    entity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.entity", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.entity", "title", "uuid"),
        },
    )
    dictionaryelement_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": False,
            "validators": [ReferenceValidator("morpcc.dictionaryelement", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.dictionaryelement", "title", "uuid"
            ),
        },
    )
    allow_invalid: typing.Optional[bool] = field(
        default=False,
        metadata={
            "title": "Allow invalid values",
            "description": "Allow values that are considered invalid by data dictionary",
        },
    )
    __unique_constraint__ = ["entity_uuid", "name"]

    __validators__ = [
        unique_attribute,
        required_if_primary_key,
        valid_dictionary_element,
    ]
