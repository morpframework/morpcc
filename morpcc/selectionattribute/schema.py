import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget
from morpcc.deform.referencewidget import ReferenceWidget
from morpfw.validator.field import valid_identifier

from ..attribute.form_validator import required_if_primary_key, unique_attribute
from ..referencedataproperty.schema import PROPERTY_TYPES


@dataclass
class SelectionAttributeSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "validators": [valid_identifier],
        },
    )

    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    referencedata_name: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "deform.widget": ReferenceWidget("morpcc.referencedata", "title", "name"),
        },
    )
    referencedata_property: typing.Optional[str] = field(
        default=None, metadata={"deform.widget": SelectWidget(values=PROPERTY_TYPES)}
    )
    required: typing.Optional[bool] = False
    primary_key: typing.Optional[bool] = False
    entity_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "required": True,
            "editable": False,
            "deform.widget": ReferenceWidget("morpcc.entity", "title", "uuid"),
        },
    )

    __unique_constraint__ = ["entity_uuid", "name"]

    __validators__ = [unique_attribute, required_if_primary_key]
