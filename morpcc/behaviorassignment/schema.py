import morpfw
from dataclasses import dataclass, field
from morpcc.deform.vocabularywidget import VocabularyWidget
import typing


@dataclass
class BehaviorAssignmentSchema(morpfw.Schema):

    behavior: typing.Optional[str] = field(default=None,
            metadata={'required': True, 'deform.widget':
            VocabularyWidget("morpcc.behaviors")})
    datamodel_uuid: typing.Optional[str] = field(
            default=None, metadata={'format': 'uuid', "required":True}
    )
