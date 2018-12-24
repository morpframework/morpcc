from ..app import App
from .model import AppRoot, StaticRoot
from webob import static
import os


@App.html(model=AppRoot, template='approot/index.pt')
def index(context, request):
    return {}


@App.view(model=StaticRoot)
def serve_static(context, request):
    path = os.path.join(os.path.dirname(__file__), '..',
                        'static', 'node_modules')
    return request.get_response(static.FileApp(os.path.join(path, context.path)))
