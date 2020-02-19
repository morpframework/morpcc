import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpcc.deform.referencewidget import ReferenceWidget


def attribute_search_url(widget, context, request):
    return request.relative_url("/relationship/+attribute-search")


@dataclass
class RelationshipSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None, metadata={"required": True, "editable": False}
    )
    title: typing.Optional[str] = field(default=None, metadata={"required": True})
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    datamodel_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "deform.widget": ReferenceWidget("morpcc.datamodel", "title", "uuid"),
        },
    )

    reference_attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "deform.widget": ReferenceWidget(
                "morpcc.attribute", "title", "uuid", get_search_url=attribute_search_url
            ),
        },
    )

    reference_search_attribute_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "deform.widget": ReferenceWidget(
                "morpcc.attribute", "title", "uuid", get_search_url=attribute_search_url
            ),
        },
    )
    required: typing.Optional[bool] = False
