import typing
from dataclasses import dataclass, field

import morpfw
from morpfw.validator.field import valid_identifier

from ..attribute.form_validator import unique_attribute
from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator
from .form_validator import valid_backrelationship


def relationship_search_url(widget, context, request):
    entity_uuid = request.GET.get("entity_uuid", None)
    baseurl = request.relative_url("/backrelationship/+relationship-search")
    if entity_uuid:
        return "{}?entity_uuid={}".format(baseurl, entity_uuid)
    return baseurl


@dataclass
class BackRelationshipSchema(morpfw.Schema):

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
    entity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Entity",
            "required": True,
            "editable": False,
            "format": "uuid",
            "validators": [ReferenceValidator("morpcc.entity", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.entity", "title", "uuid"),
        },
    )

    reference_relationship_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Reference Relationship",
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.relationship", "uuid")],
            "deform.widget": ReferenceWidget(
                "morpcc.relationship",
                "title",
                "uuid",
                get_search_url=relationship_search_url,
            ),
        },
    )

    single_relation: typing.Optional[bool] = False

    __validators__ = [unique_attribute, valid_backrelationship]
