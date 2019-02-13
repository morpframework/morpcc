from .app import App
from webob import static
from webob.exc import HTTPNotFound, HTTPUnauthorized
from pkg_resources import resource_filename
import os


class StaticRoot(object):

    module = 'morpcc'
    directory = 'static_files'

    def __init__(self, path):
        self.path = path or ''

    def resource_path(self):
        if not self.path.strip():
            return None
        d = resource_filename(self.module, self.directory)
        return os.path.join(d, self.path)


@App.path(model=StaticRoot, path='/__static__/morpcc', absorb=True)
def get_staticroot(absorb):
    return StaticRoot(absorb)


@App.view(model=StaticRoot)
def serve_static(context, request):
    path = context.resource_path()
    if not path:
        raise HTTPNotFound()
    resp = request.get_response(static.FileApp(path))
    if resp.status_code == 404:
        raise HTTPNotFound()
    if resp.status_code == 403:
        raise HTTPUnauthorized()
    return resp


class DeformStaticRoot(StaticRoot):

    module = 'deform'
    directory = 'static'


@App.path(model=DeformStaticRoot, path='/__static__/deform', absorb=True)
def get_deformstaticroot(absorb):
    return DeformStaticRoot(absorb)
