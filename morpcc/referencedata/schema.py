import morpfw
from dataclasses import dataclass
import typing


@dataclass
class ReferenceDataSchema(morpfw.Schema):

    name: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None

    __unique_constraint__ = ["name"]

