import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpfw.validator.field import valid_identifier

from ..attribute.form_validator import required_if_primary_key, unique_attribute
from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator


def attribute_search_url(widget, context, request):
    return request.relative_url("/relationship/+attribute-search")


@dataclass
class RelationshipSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "validators": [valid_identifier],
            "editable": False,
        },
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})

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

    reference_attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.attribute", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.attribute", "title", "uuid", get_search_url=attribute_search_url
            ),
        },
    )

    reference_search_attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "format": "uuid",
            "validators": [ReferenceValidator("morpcc.attribute", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.attribute", "title", "uuid", get_search_url=attribute_search_url
            ),
        },
    )

    required: typing.Optional[bool] = False
    primary_key: typing.Optional[bool] = False

    __validators__ = [unique_attribute, required_if_primary_key]
