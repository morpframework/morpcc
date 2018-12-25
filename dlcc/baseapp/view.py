import morpfw
import morepath
from morepath.authentication import NO_IDENTITY
from morpfw.auth.user.path import get_user_collection
from webob.exc import HTTPNotFound, HTTPForbidden, HTTPInternalServerError
from .app import App
from .app import SQLAuthApp
from .root import Root


@App.html(model=Root, name='login', template='master/login.pt')
def login(context, request):
    pass


@App.html(model=Root, name='login', template='master/login.pt', request_method='POST')
def process_login(context, request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    newreq = request.copy(app=SQLAuthApp())
    collection = get_user_collection(newreq)

    if not collection.authenticate(username, password):
        request.notify('error', 'Invalid Login',
                       'Please check your username / password')
        return

    @request.after
    def remember(response):
        """Remember the identity of the user logged in."""
        # We pass the extra info to the identity object.
        response.headers.add('Access-Control-Expose-Headers', 'Authorization')
        identity = morepath.Identity(username)
        request.app.remember_identity(response, request, identity)
    request.notify('success', 'Hello!', 'Welcome!!')
    return morepath.redirect(request.GET.get('came_from',
                                             request.relative_url('/')))


@App.view(model=Root, name='logout')
def logout(context, request):
    @request.after
    def forget(response):
        request.app.forget_identity(response, request)

    return morepath.redirect(request.relative_url('/'))


@App.html(model=HTTPNotFound, template='master/error_404.pt')
def httpnotfound_error(context, request):
    @request.after
    def adjust_status(response):
        response.status = 404
    return {'status': 'error',
            'message': 'Object Not Found : %s' % request.path}


@App.html(model=HTTPForbidden, template="master/error_403.pt")
def forbidden_error(context, request):
    if request.identity is NO_IDENTITY:
        return morepath.redirect('/login?came_from=%s' % request.url)

    @request.after
    def adjust_status(response):
        response.status = 403
#   FIXME: should log this when a config for DEBUG_SECURITY is enabled
#    logger.error(traceback.format_exc())
    return {'status': 'error',
            'message': 'Access Denied : %s' % request.path}
