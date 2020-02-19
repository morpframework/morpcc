# 
import typing
from dataclasses import dataclass, field

import morpfw
# 
from deform.widget import TextAreaWidget
from morpfw.validator.field import unique, valid_identifier


@dataclass
class ApplicationSchema(morpfw.Schema):

    name: typing.Optional[str] = field(
            default=None, metadata={'required': True, 'editable': False,
                'validators': [unique, valid_identifier]})
    title: typing.Optional[str] = field(
            default=None, metadata={'required': True})

    description: typing.Optional[str] = field(
            default=None, metadata={'format': 'text'}
    )