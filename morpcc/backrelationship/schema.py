import typing
from dataclasses import dataclass, field

import morpfw
from morpcc.deform.referencewidget import ReferenceWidget
from morpfw.validator.field import valid_identifier

from ..attribute.form_validator import unique_attribute


def relationship_search_url(widget, context, request):
    datamodel_uuid = request.GET.get("datamodel_uuid", None)
    baseurl = request.relative_url("/backrelationship/+relationship-search")
    if datamodel_uuid:
        return "{}?datamodel_uuid={}".format(baseurl, datamodel_uuid)
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
    datamodel_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "format": "uuid",
            "deform.widget": ReferenceWidget("morpcc.datamodel", "title", "uuid"),
        },
    )

    reference_relationship_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "deform.widget": ReferenceWidget(
                "morpcc.relationship",
                "title",
                "uuid",
                get_search_url=relationship_search_url,
            ),
        },
    )

    __validators__ = [unique_attribute]
