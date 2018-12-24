import os
import morpfw
from morpfw.app import DBSessionRequest
from morpfw.auth.app import App as AuthApp
from more.chameleon import ChameleonApp
import bowerstatic
import functools


class App(ChameleonApp, morpfw.SQLApp):
    pass


@App.template_render(extension='.pt')
def get_chameleon_render(loader, name, original_render):

    template = loader.load(name, 'xml')

    def render(content, request):
        main_template = loader.load('master/main_template.pt', 'xml')
        load_template = functools.partial(loader.load, format='xml')
        variables = {'request': request,
                     'main_template': main_template,
                     'app': request.app,
                     'settings': request.app.settings,
                     'load_template': load_template}
        variables.update(content)
        return original_render(template.render(**variables), request)
    return render


@App.template_directory()
def get_template_directory():
    return 'templates'
