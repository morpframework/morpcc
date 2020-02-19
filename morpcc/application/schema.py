import morpfw
from dataclasses import dataclass, field
# 
from deform.widget import TextAreaWidget
# 
import typing


@dataclass
class ApplicationSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
            default=None, metadata={'required': True, 'editable': False})
    title: typing.Optional[str] = field(
            default=None, metadata={'required': True})

    description: typing.Optional[str] = field(
            default=None, metadata={'format': 'text'}
    )

