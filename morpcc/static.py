from .app import App
from webob import static
from pkg_resources import resource_filename
import os


class StaticRoot(object):

    module = 'morpcc'
    directory = 'static_files'

    def __init__(self, path):
        self.path = path

    def resource_path(self):
        d = resource_filename(self.module, self.directory)
        return os.path.join(d, self.path)


@App.path(model=StaticRoot, path='/static', absorb=True)
def get_staticroot(absorb):
    return StaticRoot(absorb)


@App.view(model=StaticRoot)
def serve_static(context, request):
    return request.get_response(static.FileApp(context.resource_path()))


class DeformStaticRoot(StaticRoot):

    module = 'deform'
    directory = 'static'


@App.path(model=DeformStaticRoot, path='/deform_static', absorb=True)
def get_deformstaticroot(absorb):
    return DeformStaticRoot(absorb)
