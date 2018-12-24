from .app import App
from webob import static
import os


class StaticRoot(object):

    def __init__(self, path):
        self.path = path


@App.path(model=StaticRoot, path='/static', absorb=True)
def get_staticroot(absorb):
    return StaticRoot(absorb)


@App.view(model=StaticRoot)
def serve_static(context, request):
    path = os.path.join(os.path.dirname(__file__),
                        'static_files', 'node_modules')
    return request.get_response(static.FileApp(os.path.join(path, context.path)))
