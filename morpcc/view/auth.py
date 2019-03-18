from morpfw.authn.pas.user.path import get_user_collection
import morepath
from ..app import App
from ..app import SQLAuthApp
from ..root import Root
import html
import urllib.parse
from dataclasses import dataclass, field
from ..util import dataclass_to_colander
import deform


@dataclass
class LoginForm(object):

    username: str = field(metadata={'required': True})
    password: str = field(metadata={'required': True})


@App.html(model=Root, name='login', template='master/login.pt')
def login(context, request):
    pass


@App.html(model=Root, name='login', template='master/login.pt', request_method='POST')
def process_login(context, request):
    controls = list(request.POST.items())
    formschema = dataclass_to_colander(LoginForm)
    form = deform.Form(formschema())
    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True

    if not failed:
        username = data['username']
        password = data['password']
        newreq = request.get_authn_request()
        collection = get_user_collection(newreq)

        if not collection.authenticate(username, password):
            request.notify('error', 'Invalid Login',
                           'Please check your username / password')
            return

        @request.after
        def remember(response):
            """Remember the identity of the user logged in."""
            # We pass the extra info to the identity object.
            response.headers.add(
                'Access-Control-Expose-Headers', 'Authorization')
            u = collection.get(username)
            identity = morepath.Identity(u.userid)
            request.app.remember_identity(response, request, identity)
        came_from = request.GET.get('came_from', '')
        if came_from:
            came_from = urllib.parse.unquote(came_from)
        else:
            came_from = request.relative_url('/')
        return morepath.redirect(came_from)

    request.notify('error', 'Invalid Login',
                   'Please check your username / password')


@App.view(model=Root, name='logout')
def logout(context, request):
    @request.after
    def forget(response):
        request.app.forget_identity(response, request)

    return morepath.redirect(request.relative_url('/'))


@dataclass
class RegistrationForm(object):
    username: str = field(metadata={'required': True})
    email: str = field(metadata={'required': True})
    password: str = field(metadata={'required': True})
    password_validate: str = field(metadata={'required': True})


@App.view(model=Root, name='register', request_method='POST')
def process_register(context, request):

    controls = list(request.POST.items())
    formschema = dataclass_to_colander(RegistrationForm)
    form = deform.Form(formschema())
    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True

    if not failed:
        newreq = request.get_authn_request()
        collection = get_user_collection(newreq)
        if data['password'] != data['password_validate']:
            request.notify('error', 'Password does not match',
                           'Please check your password')
            return morepath.redirect(request.relative_url('/login#signup'))

        username = data['username']
        email = data['email']
        if collection.get(username):
            request.notify('error', 'Username already taken',
                           'Please use a different username')
            return morepath.redirect(request.relative_url('/login#signup'))

        if collection.get_by_email(email):
            request.notify('error', 'Email already registered',
                           'Log-in using your existing account')
            return morepath.redirect(request.relative_url('/login#signup'))

        del data['password_validate']
        user = collection.create(data)
        request.notify('success', 'Registration successful',
                       'You may log-in using your account now')
        return morepath.redirect(request.relative_url('/login'))
