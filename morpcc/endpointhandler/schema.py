import typing
from dataclasses import dataclass, field

import morpfw
from deform.widget import SelectWidget

from ..deform.codewidget import CodeWidget
from ..deform.referencewidget import ReferenceWidget
from ..validator.reference import ReferenceValidator

ALLOWED_METHODS: list = ["GET", "POST", "PATCH", "DELETE"]


def valid_method(request, schema, field, value, mode=None):
    if value not in ALLOWED_METHODS:
        return "Invalid method"


@dataclass
class EndpointHandlerSchema(morpfw.Schema):

    endpoint_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Endpoint",
            "format": "uuid",
            "required": True,
            "index": True,
            "deform.widget": ReferenceWidget(
                "morpcc.endpoint", term_field="title", value_field="uuid"
            ),
            "validators": [ReferenceValidator("morpcc.endpoint", "uuid")],
        },
    )

    method: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "index": True,
            "deform.widget": SelectWidget(values=[(k, k) for k in ALLOWED_METHODS]),
            "validators": [valid_method],
        },
    )
    code: typing.Optional[str] = field(
        default="def handle(context, request):\n    return True",
        metadata={
            "format": "text/python",
            "required": True,
            "deform.widget": CodeWidget(),
        },
    )

    __unique_constraint__ = ["endpoint_uuid", "method"]
