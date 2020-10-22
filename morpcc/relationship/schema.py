import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpcc.crud.model import CollectionUI, ModelUI
from morpfw.crud.model import Collection, Model
from morpfw.validator.field import valid_identifier

from ..attribute.form_validator import required_if_primary_key, unique_attribute
from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator
from .form_validator import valid_search_attribute


def attribute_search_url(widget, context, request):
    if isinstance(context, Model):
        entity_uuid = context["entity_uuid"]
    elif isinstance(context, ModelUI):
        entity_uuid = context.model["entity_uuid"]
    else:
        entity_uuid = request.GET.get("entity_uuid")
    entitycol = request.get_collection("morpcc.entity")
    entity = entitycol.get(entity_uuid)
    return request.relative_url(
        "/relationship/+attribute-search?schema_uuid=%s" % entity["schema_uuid"]
    )


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
            "title": "Entity",
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
            "title": "Reference Attribute",
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
            "title": "Reference Search Attribute",
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

    __validators__ = [unique_attribute, required_if_primary_key, valid_search_attribute]
