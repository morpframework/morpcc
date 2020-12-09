import html

from .app import App
from .permission import ViewHome


class Root(object):
    def __init__(self, request):
        self.request = request


@App.path(model=Root, path="/")
def get_root(request):
    return Root(request)


@App.html(model=Root, permission=ViewHome, template="master/index.pt")
def index(context, request):
    return {
        "page_title": "Applications",
        "applications": request.get_collection("morpcc.application").all(),
    }
