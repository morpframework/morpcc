from ..app import App
from .model import DictionaryEntityCollection, DictionaryEntityModel

#
from .modelui import DictionaryEntityCollectionUI, DictionaryEntityModelUI
from .path import get_collection, get_model
from .schema import DictionaryEntitySchema

#


@App.typeinfo(name="morpcc.dictionaryentity", schema=DictionaryEntitySchema)
def get_typeinfo(request):
    return {
        "title": "DictionaryEntity",
        "description": "DictionaryEntity type",
        "schema": DictionaryEntitySchema,
        "collection": DictionaryEntityCollection,
        "collection_factory": get_collection,
        "model": DictionaryEntityModel,
        "model_factory": get_model,
        #
        "collection_ui": DictionaryEntityCollectionUI,
        "model_ui": DictionaryEntityModelUI,
        "internal": True
        #
    }
