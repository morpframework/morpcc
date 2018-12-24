from morpfw.crud import permission
from ..app import App
from .model import AppRoot
from webob import static
import os


@App.html(model=AppRoot, template='approot/index.pt', permission=permission.View)
def index(context, request):
    return {}
