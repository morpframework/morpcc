import morpfw
from dataclasses import dataclass
import typing


@dataclass
class SettingSchema(morpfw.Schema):

    key: typing.Optional[str] = None
    value: typing.Optional[str] = None
