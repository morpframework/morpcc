import html
from .app import App


class Root(object):

    def __init__(self, request):
        self.request = request


@App.path(model=Root, path='/')
def get_root(request):
    return Root(request)


class ModelUI(object):

    def __init__(self, request, model):
        self.request = request
        self.model = model


class CollectionUI(object):

    modelui_class = ModelUI

    @property
    def page_title(self):
        return str(self.collection.__class__.__name__)

    @property
    def listing_title(self):
        return 'Contents'

    columns = [
        {'title': 'Type', 'name': 'structure:type'},
        {'title': 'Object', 'name': 'structure:object_string'},
        {'title': 'UUID', 'name': 'uuid'},
        {'title': 'Created', 'name': 'created'},
        {'title': 'State', 'name': 'state'},
        {'title': 'Actions', 'name': 'structure:buttons'},
    ]

    def get_buttons(self, obj, request):
        buttons = [{
            'icon': 'eye',
            'url': request.link(self.modelui_class(request, obj)),
            'title': 'View'
        }, {
            'icon': 'pencil',
            'url': request.link(self.modelui_class(request, obj), '+edit'),
            'title': 'Edit'
        }, {
            'icon': 'trash',
            'url': request.link(self.modelui_class(request, obj), '+delete'),
            'title': 'Delete'
        }]
        return buttons

    def __init__(self, request, collection):
        self.request = request
        self.collection = collection

    def get_structure_column(self, obj, request, column_type):
        column_type = column_type.replace('structure:', '')
        if column_type == 'type':
            return str(obj.__class__.__name__)
        elif column_type == 'object_string':
            return html.escape(str(obj))
        elif column_type == 'buttons':
            results = ''
            for button in self.get_buttons(obj, request):
                results += ('<a title="%(title)s" href="%(url)s">'
                            '<i class="fa fa-%(icon)s">'
                            '</i></a> ') % button
            return results
        return ''
