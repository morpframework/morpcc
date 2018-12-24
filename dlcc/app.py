import morpfw
from morpfw.auth.app import App as AuthApp
from .baseapp.app import App as BaseApp


class App(BaseApp):
    pass


class SQLAuthApp(AuthApp, morpfw.SQLApp):
    pass


@App.mount(app=SQLAuthApp, path='/api/v1/auth/')
def get_auth_app():
    return SQLAuthApp()


@App.template_directory()
def get_template_directory():
    return 'templates'
