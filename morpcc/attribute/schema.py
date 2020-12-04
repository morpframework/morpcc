import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import (
    AutocompleteInputWidget,
    HiddenWidget,
    Select2Widget,
    SelectWidget,
)
from morpfw import request
from morpfw.validator.field import valid_identifier

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator
from .form_validator import (
    required_if_primary_key,
    unique_attribute,
    valid_dictionary_element,
    valid_searchable_type,
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
    ("boolean", "Boolean"),
)


def valid_type(request, schema, field, value, mode=None):
    if value not in [k for k, v in ACCEPTED_TYPES]:
        return "Invalid type"


def get_schemata_widget(request):
    col = request.get_collection("morpcc.attribute")
    agg = col.aggregate(
        group={"schemata": "schemata", "total": {"function": "count", "field": "id"},}
    )
    schematas = []
    for a in agg:
        if a["schemata"] is not None:
            schematas.append(a["schemata"])
    for d in ["default", "hidden"]:
        if d not in schematas:
            schematas.append(d)
    return Select2Widget(values=[(k, k) for k in schematas], tags=True, placeholder="")


@dataclass
class AttributeSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "searchable": True,
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
    title: typing.Optional[str] = field(
        default=None, metadata={"required": True, "searchable": True}
    )
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
            "title": "Entity",
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
            "title": "Dictionary Element",
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

    searchable: typing.Optional[bool] = field(
        default=False,
        metadata={
            "title": "Searchable",
            "description": "Make this attribute searchable",
        },
    )

    schemata: typing.Optional[str] = field(
        default="default",
        metadata={
            "title": "Field Schemata",
            "required": True,
            "deform.widget_factory": get_schemata_widget,
        },
    )
    order: typing.Optional[int] = field(
        default=0, metadata={"title": "Ordering Index", "editable": False,},
    )

    __unique_constraint__ = ["entity_uuid", "name", "deleted"]

    __validators__ = [
        unique_attribute,
        required_if_primary_key,
        valid_dictionary_element,
        valid_searchable_type,
    ]

    __references__ = [
        morpfw.Reference("entity_uuid", "morpcc.entity"),
        morpfw.Reference("dictionaryelement_uuid", "morpcc.dictionaryelement"),
    ]
