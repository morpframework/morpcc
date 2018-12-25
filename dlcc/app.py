import morpfw
from morpfw.auth.app import App as AuthApp
from .baseapp.app import App as BaseApp


class App(BaseApp):
    pass


@App.template_directory()
def get_template_directory():
    return 'templates'
