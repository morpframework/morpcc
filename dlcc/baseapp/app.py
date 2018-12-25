import os
import morpfw
from morpfw.app import DBSessionRequest
from morpfw.auth.app import App as AuthApp
from more.chameleon import ChameleonApp
import morepath
from morepath.publish import resolve_model
from morpfw.main import create_app, create_sqlapp
from beaker.middleware import SessionMiddleware
import functools


class WebAppRequest(DBSessionRequest):

    def notify(self, category, title, message):
        session = self.environ['beaker.session']
        session.setdefault('messages', [])
        session['messages'].append({'category': category, 'title': title,
                                    'message': message})

    def messages(self):
        session = self.environ['beaker.session']
        result = session.get('messages', [])
        session['messages'] = []
        return result


class App(ChameleonApp, morpfw.SQLApp):

    request_class = WebAppRequest


class SQLAuthApp(AuthApp, morpfw.SQLApp):
    pass


@App.mount(app=SQLAuthApp, path='/api/v1/auth/')
def get_auth_app():
    return SQLAuthApp()


@create_app.register(app=App)
def create_web_app(app, settings, scan=True, **kwargs):
    application = create_sqlapp(
        app=app, settings=settings, scan=scan, **kwargs)
    return SessionMiddleware(application, settings['beaker_session'])
