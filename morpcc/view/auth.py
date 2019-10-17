from morpfw.authn.pas.user.path import get_user_collection
import morepath
from ..app import App
from ..root import Root
import html
import urllib.parse
from dataclasses import dataclass, field
from ..util import dataclass_to_colander
import deform


@dataclass
class LoginForm(object):

    username: str = field(metadata={'required': True})
    password: str = field(metadata={'required': True,
                                    'deform': {
                                        'widget': deform.widget.PasswordWidget()
                                    }})


@App.html(model=Root, name='login', template='master/anon-form.pt')
def login(context, request):
    formschema = dataclass_to_colander(LoginForm)
    return {
        'form_title': 'Login',
        'form': deform.Form(formschema(),
                            buttons=('Login',
                                     deform.Button('register', title='Register', type='link',
                                                   value=request.relative_url('/register'))))
    }


@App.html(model=Root, name='login', template='master/anon-form.pt', request_method='POST')
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
        username = data['username'].lower()
        password = data['password']
        collection = get_user_collection(request)

        if not collection.authenticate(username, password):
            request.notify('error', 'Invalid Login',
                           'Please check your username / password')
            return morepath.redirect(request.relative_url('/login'))

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

    return morepath.redirect(request.relative_url('/login'))


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
    password: str = field(metadata={'required': True,
                                    'deform': {
                                        'widget': deform.widget.PasswordWidget()
                                    }})
    password_validate: str = field(metadata={'required': True,
                                             'deform': {
                                                 'widget': deform.widget.PasswordWidget()
                                             }})


@App.html(model=Root, name='register', template='master/nologin-form.pt')
def register(context, request):
    schema = dataclass_to_colander(RegistrationForm)
    return {
        'form_title': 'Register',
        'form': deform.Form(schema(), buttons=('Register',
                                               deform.Button('login', title='Login', type='link',
                                                             value=request.relative_url('/login'))))
    }


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
        collection = get_user_collection(request)
        if data['password'] != data['password_validate']:
            request.notify('error', 'Password does not match',
                           'Please check your password')
            return morepath.redirect(request.relative_url('/register'))

        username = data['username'].lower()
        email = data['email']
        if collection.get(username):
            request.notify('error', 'Username already taken',
                           'Please use a different username')
            return morepath.redirect(request.relative_url('/register'))

        if collection.get_by_email(email):
            request.notify('error', 'Email already registered',
                           'Log-in using your existing account')
            return morepath.redirect(request.relative_url('/register'))

        del data['password_validate']
        data['username'] = data['username'].lower()
        user = collection.create(data)

        @request.after
        def remember(response):
            """Remember the identity of the user logged in."""
            # We pass the extra info to the identity object.
            response.headers.add(
                'Access-Control-Expose-Headers', 'Authorization')
            identity = morepath.Identity(user.userid)
            request.app.remember_identity(response, request, identity)
        return morepath.redirect(request.relative_url('/'))
