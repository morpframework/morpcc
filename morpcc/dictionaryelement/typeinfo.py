from ..app import App
from .model import DictionaryElementCollection, DictionaryElementModel

#
from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI
from .path import get_collection, get_model
from .schema import DictionaryElementSchema

#


@App.typeinfo(name="morpcc.dictionaryelement", schema=DictionaryElementSchema)
def get_typeinfo(request):
    return {
        "title": "DictionaryElement",
        "description": "DictionaryElement type",
        "schema": DictionaryElementSchema,
        "collection": DictionaryElementCollection,
        "collection_factory": get_collection,
        "model": DictionaryElementModel,
        "model_factory": get_model,
        #
        "collection_ui": DictionaryElementCollectionUI,
        "model_ui": DictionaryElementModelUI,
        "internal": True
        #
    }
