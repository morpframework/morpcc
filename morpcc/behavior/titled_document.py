from ..app import App
from .base import BaseBehavior
from dataclasses import dataclass, field
import typing

@dataclass
class TitledDocumentSchema(object):
    title: typing.Optional[str] = field(default=None, 
            metadata={'required': True})
    description: typing.Optional[str] = field(default=None,
            metadata={'format': 'text'})

class TitledDocumentModel(object):
    pass

class TitledDocumentModelUI(object):
    pass

class TitledDocumentCollection(object):
    pass

class TitledDocumentCollectionUI(object):
    pass

class TitledDocumentBehavior(BaseBehavior):

    schema = TitledDocumentSchema
    model_marker = TitledDocumentModel
    modelui_marker = TitledDocumentModelUI
    collection_marker = TitledDocumentCollection
    collectionui_marker = TitledDocumentCollectionUI


@App.behavior('morpcc.behavior.titled_document')
def get_behavior(request):
    return TitledDocumentBehavior
