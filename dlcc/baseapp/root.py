from .app import App


class Root(object):

    def __init__(self, request):
        self.request = request


@App.path(model=Root, path='/')
def get_root(request):
    return Root(request)


class CollectionUI(object):

    page_title = 'Page Title'

    def __init__(self, request, collection):
        self.request = request
        self.collection = collection


class ModelUI(object):

    def __init__(self, request, model):
        self.request = request
        self.model = model
