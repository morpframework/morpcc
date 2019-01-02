from .model import APIKeyModelUI, APIKeyCollectionUI
from ..app import App
from morpfw.authn.pas.apikey.path import get_apikey, get_apikey_collection


@App.path(model=APIKeyCollectionUI, path='/manage-apikeys')
def get_apikey_collection_ui(request):
    newreq = request.get_authn_request()
    col = get_apikey_collection(newreq)
    return APIKeyCollectionUI(newreq, col)


@App.path(model=APIKeyModelUI, path='/manage-apikeys/{apikeyname}',
          variables=lambda obj: {'apikeyname': obj.model.data['apikeyname']})
def get_apikey_model_ui(request, apikeyname):
    newreq = request.get_authn_request()
    apikey = get_apikey(newreq, apikeyname)
    col = get_apikey_collection(newreq)
    return APIKeyModelUI(newreq, apikey, APIKeyCollectionUI(newreq, col))
