import os
import morpfw
from morpfw.app import DBSessionRequest
from morpfw.authn.pas.policy import SQLStorageAuthnPolicy, SQLStorageAuthApp
from morpfw.authz.pas import DefaultAuthzPolicy
from .authn import IdentityPolicy
from more.chameleon import ChameleonApp
import morepath
from morepath.publish import resolve_model
from morpfw.main import create_app, create_sqlapp
from beaker.middleware import SessionMiddleware as BeakerMiddleware
import functools
import dectate
import reg
from . import directive
from uuid import uuid4


class MorpBeakerMiddleware(BeakerMiddleware):

    def initdb(self):
        self.app.initdb()


class WebAppRequest(DBSessionRequest):

    def notify(self, category, title, message):
        session = self.environ['beaker.session']
        session.setdefault('messages', [])
        session['messages'].append({'category': category, 'title': title,
                                    'message': message})
        session.save()

    def messages(self):
        session = self.environ['beaker.session']
        result = session.get('messages', [])
        session['messages'] = []
        session.save()
        return result

    @property
    def session(self):
        return self.environ['beaker.session']


class App(ChameleonApp, morpfw.SQLApp, DefaultAuthzPolicy):

    request_class = WebAppRequest

    portlet = dectate.directive(directive.PortletFactoryAction)
    portletprovider = dectate.directive(directive.PortletProviderFactoryAction)
    structure_column = dectate.directive(directive.StructureColumnAction)
    schemaextender = dectate.directive(directive.SchemaExtenderAction)

    @reg.dispatch_method(reg.match_instance('model'),
                         reg.match_instance('request'),
                         reg.match_key('name'))
    def get_structure_column(self, model, request, name):
        raise NotImplementedError(
            'Get structure columns for %s structure:%s' % (model, name))

    def get_portletprovider(self, name):
        return self.config.portletprovider_registry.get_provider(name)

    @reg.dispatch_method(reg.match_class('schema'))
    def get_schemaextender(self, schema):
        return schema


class AuthnPolicy(SQLStorageAuthnPolicy):

    def get_identity_policy(self, settings):
        if settings.application.development_mode:
            secure = False
        else:
            secure = True

        master_secret = getattr(
            settings.security, 'master_secret', uuid4().hex)

        jwt_settings = settings.security.jwt.copy()
        if not 'master_secret' in jwt_settings:
            jwt_settings['master_secret'] = master_secret

        itsdangerous_settings = {
            'secure': secure,
            'secret': master_secret
        }

        return IdentityPolicy(
            jwt_settings=jwt_settings,
            itsdangerous_settings=itsdangerous_settings,
            api_root='/api',
            development_mode=settings.application.development_mode)


App.hook_auth_models(prefix='/api/v1/auth')


@create_app.register(app=App)
def create_web_app(app, settings, scan=True, **kwargs):
    application = create_sqlapp(
        app=app, settings=settings, scan=scan, **kwargs)
    if (settings['beaker_session'].get('session.type', None) is None and
            settings['beaker_session'].get('session.url', None) is None):
        settings['beaker_session']['session.type'] = 'ext:database'
        settings['beaker_session']['session.url'] = (
            settings['application']['dburi'])

    return MorpBeakerMiddleware(application, settings['beaker_session'])
