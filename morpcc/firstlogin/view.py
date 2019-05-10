from ..app import App
from ..root import Root
from ..permission import ViewHome
from morpfw.authn.pas.user.path import get_user_collection
import morepath


@App.view(model=Root, name='firstlogin', permission=ViewHome)
def firstlogin(context, request):
    return
