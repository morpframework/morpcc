import typing
from dataclasses import dataclass, field

import morpfw
from morpfw.crud.field import Field
from morpfw.validator.field import valid_identifier

from ..deform.referencewidget import ReferenceWidget
from ..deform.vocabularywidget import VocabularyWidget
from ..validator.reference import ReferenceValidator
from ..validator.vocabulary import VocabularyValidator


def only_one_primary(request, schema, data, mode=None, **kw):
    if data["is_primary"] is True:
        schema_uuid = data["schema_uuid"]
        schemacol = request.get_collection("morpcc.schema")
        schema = schemacol.get(schema_uuid)
        for entity in schema.entities():
            if entity["name"] != data["name"]:
                if entity["is_primary"]:
                    return {
                        "field": "name",
                        "message": (
                            "Only one primary entity is allowed. "
                            "Current primary entity is '{}'"
                        ).format(entity["name"]),
                    }


@dataclass
class EntitySchema(morpfw.Schema):
    name: typing.Optional[str] = field(
        default=None,
        metadata={
            "required": True,
            "editable": False,
            "validators": [valid_identifier],
        },
    )
    title: typing.Optional[str] = Field().default(None).required().init()
    description: typing.Optional[str] = field(default=None, metadata={"format": "text"})
    icon: typing.Optional[str] = field(
        default=None,
        metadata={
            "validators": [VocabularyValidator("morpcc.fa-icons")],
            "deform.widget": VocabularyWidget("morpcc.fa-icons"),
        },
    )

    allow_invalid: typing.Optional[bool] = False

    schema_uuid: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Schema",
            "format": "uuid",
            "required": True,
            "editable": False,
            "validators": [ReferenceValidator("morpcc.schema", "uuid")],
            "deform.widget": ReferenceWidget("morpcc.schema", "title", "uuid"),
        },
    )

    is_primary: typing.Optional[bool] = field(
        default=False, metadata={"title": "Is Primary Entity", "required": False},
    )

    __validators__ = [only_one_primary]
    __unique_constraint__ = ["schema_uuid", "name", "deleted"]
    __references__ = [morpfw.Reference("schema_uuid", "morpcc.schema")]
    __backreferences__ = [
        morpfw.BackReference(
            "attributes", "morpcc.attribute", "entity_uuid", title="Attributes"
        ),
        morpfw.BackReference(
            "entity_validators",
            "morpcc.entityvalidatorassignment",
            "entity_uuid",
            title="Entity Validators",
        ),
    ]
