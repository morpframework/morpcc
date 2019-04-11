from ..app import App
from ..root import Root
from ..permission import ViewHome
from morpfw.authn.pas.user.path import get_user_collection
import morepath


@App.view(model=Root, name='firstlogin', permission=ViewHome)
def firstlogin(context, request):
    usercol = get_user_collection(request.get_authn_request())
    user = usercol.get_by_userid(request.identity.userid)
    sm = user.statemachine()
    sm.initialize()
    request.notify('info', 'User initialized',
                   'Congratulations, your user have been initialized')
    return morepath.redirect(request.relative_url('/'))
