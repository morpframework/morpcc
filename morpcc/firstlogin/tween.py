from ..app import App
from morpfw.authn.pas.path import get_user_collection
import morepath


@App.tween_factory()
def make_tween(app, handler):
    def redirect_to_firstlogin(request: morepath.Request):
        if request.path.startswith('/__static__/'):
            return handler(request)
        if request.path == '/logout':
            return handler(request)
        userid = request.identity.userid
        if userid:
            col = get_user_collection(request)
            userobj = col.get_by_userid(userid)
            if userobj['state'] == 'new' and not request.path.startswith('/firstlogin'):
                resp = morepath.redirect(request.relative_url('/firstlogin'))
                resp.headers['Cache-Control'] = 'no-store'
                return resp
        return handler(request)
    return redirect_to_firstlogin
