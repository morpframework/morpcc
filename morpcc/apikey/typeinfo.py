from ..app import App
from morpfw.authn.pas.apikey.typeinfo import get_typeinfo as get_basetypeinfo
from .model import APIKeyCollectionUI, APIKeyModelUI
from .path import get_apikey_collection_ui, get_apikey_model_ui


@App.typeinfo('morpfw.pas.apikey')
def get_typeinfo(request):
    ti = get_basetypeinfo(request)
    ti['collection_ui'] = APIKeyCollectionUI
    ti['model_ui'] = APIKeyModelUI
    ti['collection_ui_factory'] = get_apikey_collection_ui
    ti['model_ui_factory'] = get_apikey_model_ui
    return ti
