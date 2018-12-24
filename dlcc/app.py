import os
import morpfw
from morpfw.app import DBSessionRequest
from morpfw.auth.app import App as AuthApp
from more.chameleon import ChameleonApp
import bowerstatic


class SQLAuthApp(AuthApp, morpfw.SQLApp):
    pass


class App(ChameleonApp, morpfw.SQLApp):
    pass


@App.template_render(extension='.pt')
def get_chameleon_render(loader, name, original_render):

    template = loader.load(name, 'xml')

    def render(content, request):
        main_template = loader.load('main_template.pt', 'xml')
        variables = {'request': request, 'main_template': main_template}
        variables.update(content)
        return original_render(template.render(**variables), request)
    return render


@App.template_directory()
def get_template_directory():
    return 'templates'


@App.mount(app=SQLAuthApp, path='/api/v1/auth/')
def get_auth_app():
    return SQLAuthApp()
