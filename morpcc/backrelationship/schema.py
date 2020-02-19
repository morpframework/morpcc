import typing
from dataclasses import dataclass, field

import morpfw
from morpcc.deform.referencewidget import ReferenceWidget


def relationship_search_url(widget, context, request):
    datamodel_uuid = request.GET.get("datamodel_uuid", None)
    baseurl = request.relative_url("/backrelationship/+relationship-search")
    if datamodel_uuid:
        return "{}?datamodel_uuid={}".format(baseurl, datamodel_uuid)
    return baseurl


@dataclass
class BackRelationshipSchema(morpfw.Schema):

    name: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    datamodel_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "deform.widget": ReferenceWidget("morpcc.datamodel", "title", "uuid"),
        },
    )

    reference_relationship_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "deform.widget": ReferenceWidget(
                "morpcc.relationship",
                "title",
                "uuid",
                get_search_url=relationship_search_url,
            ),
        },
    )
