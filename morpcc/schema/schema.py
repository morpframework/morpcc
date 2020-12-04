import typing
from dataclasses import dataclass, field

import morpfw


@dataclass
class SchemaSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
        default=None, metadata={"required": True, "unique": True}
    )
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None

    __unique_constraint__ = ["name", "deleted"]
    __backreferences__ = [
        morpfw.BackReference(
            "applications", "morpcc.application", "schema_uuid", title="Applications"
        ),
        morpfw.BackReference(
            "entities", "morpcc.entity", "schema_uuid", title="Entities",
        ),
    ]
