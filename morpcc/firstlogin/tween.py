from ..app import App
from morpfw.authn.pas.path import get_user_collection
import morepath


@App.tween_factory()
def make_tween(app, handler):
    def redirect_to_firstlogin(request: morepath.Request):
        if request.path.startswith('/__static__/'):
            return handler(request)
        userid = request.identity.userid
        if userid:
            col = get_user_collection(request)
            userobj = col.get_by_userid(userid)
            if userobj['state'] == 'new' and not request.path.startswith('/firstlogin'):
                return morepath.redirect(request.relative_url('/firstlogin'))
        return handler(request)
    return redirect_to_firstlogin
