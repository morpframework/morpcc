import html

from .app import App
from .application.path import get_collection as get_app_collection
from .permission import ViewHome


class Root(object):
    def __init__(self, request):
        self.request = request


@App.path(model=Root, path="/")
def get_root(request):
    return Root(request)


@App.html(model=Root, permission=ViewHome, template="master/index.pt")
def index(context, request):
    return {"applications": get_app_collection(request).search()}
