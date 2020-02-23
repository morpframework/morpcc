from ..app import App
from .model import DictionaryElementCollection, DictionaryElementModel

#
from .modelui import DictionaryElementCollectionUI, DictionaryElementModelUI
from .path import get_collection, get_collection_ui, get_model, get_model_ui
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
        "collection_ui_factory": get_collection_ui,
        "model_ui": DictionaryElementModelUI,
        "model_ui_factory": get_model_ui,
        #
    }
