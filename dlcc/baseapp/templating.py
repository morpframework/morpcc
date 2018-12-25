import os
import morpfw
import morepath
from morepath.publish import resolve_model
import functools
from pkg_resources import resource_filename
from deform import Form


from .app import App
from .root import Root


@App.template_render(extension='.pt')
def get_chameleon_render(loader, name, original_render):

    template = loader.load(name, 'xml')

    def render(content, request: morepath.Request):
        main_template = loader.load('master/main_template.pt', 'xml')
        load_template = functools.partial(loader.load, format='xml')
        context = resolve_model(request)
        variables = {'request': request,
                     'context': context,
                     'main_template': main_template,
                     'app': request.app,
                     'settings': request.app.settings,
                     'load_template': load_template}
        variables.update(content or {})
        return original_render(template.render(**variables), request)
    return render


@App.template_directory()
def get_template_directory():
    return 'templates'


def set_deform_override():
    deform_templates = resource_filename('deform', 'templates')
    form_templates = resource_filename(
        'dlcc.baseapp', os.path.join('templates', 'deform'))
    search_path = (form_templates, deform_templates)
    Form.set_zpt_renderer(search_path)


set_deform_override()
