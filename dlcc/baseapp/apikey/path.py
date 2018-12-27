from .model import APIKeyModelUI, APIKeyCollectionUI
from ..app import App
from morpfw.auth.apikey.path import get_apikey, get_apikey_collection


@App.path(model=APIKeyCollectionUI, path='/manage-apikeys')
def get_apikey_collection_ui(request):
    authapp = request.app.get_authnz_provider()
    authapp.root = request.app
    newreq = request.copy(app=authapp)
    col = get_apikey_collection(newreq)
    return APIKeyCollectionUI(newreq, col)


@App.path(model=APIKeyModelUI, path='/manage-apikeys/{apikeyname}',
          variables=lambda obj: {'apikeyname': obj.model.data['apikeyname']})
def get_apikey_model_ui(request, apikeyname):
    authapp = request.app.get_authnz_provider()
    authapp.root = request.app
    newreq = request.copy(app=authapp)
    apikey = get_apikey(newreq, apikeyname)
    return APIKeyModelUI(newreq, apikey)
