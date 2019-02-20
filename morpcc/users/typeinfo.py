from ..app import App
from morpfw.authn.pas.user.typeinfo import get_typeinfo as get_basetypeinfo
from .model import UserCollectionUI, UserModelUI
from .path import get_user_collection_ui, get_user_model_ui


@App.typeinfo('morpfw.pas.user')
def get_typeinfo(request):
    ti = get_basetypeinfo(request)
    ti['collection_ui'] = UserCollectionUI
    ti['model_ui'] = UserModelUI
    ti['collection_ui_factory'] = get_user_collection_ui
    ti['model_ui_factory'] = get_user_model_ui
    return ti
