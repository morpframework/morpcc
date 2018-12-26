import html
from .app import App


class Root(object):

    def __init__(self, request):
        self.request = request


@App.path(model=Root, path='/')
def get_root(request):
    return Root(request)


class CollectionUI(object):

    page_title = 'Page Title'
    columns = [
        {'title': 'Type', 'name': 'structure:type'},
        {'title': 'Object', 'name': 'structure:object_string'},
        {'title': 'UUID', 'name': 'uuid'},
        {'title': 'Created', 'name': 'created'},
        {'title': 'State', 'name': 'state'},
    ]

    def __init__(self, request, collection):
        self.request = request
        self.collection = collection

    def get_structure_column(self, obj, request, column_type):
        column_type = column_type.replace('structure:', '')
        if column_type == 'type':
            return str(obj.__class__.__name__)
        elif column_type == 'object_string':
            return html.escape(str(obj))
        return ''


class ModelUI(object):

    def __init__(self, request, model):
        self.request = request
        self.model = model
