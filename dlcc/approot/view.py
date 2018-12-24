from ..app import App
from .model import AppRoot
from webob import static
import os


@App.html(model=AppRoot, template='approot/index.pt')
def index(context, request):
    return {}
