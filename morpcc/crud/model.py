import html


class ModelUI(object):

    view_include_fields: list = []
    view_exclude_fields: list = []
    edit_include_fields: list = []
    edit_exclude_fields: list = [
        'id', 'uuid', 'creator', 'created', 'modified', 'state', 'deleted',
        'xattrs', 'blobs'
    ]

    default_view = 'view'

    @property
    def identifier(self):
        return self.model.identifier

    def __init__(self, request, model, collection_ui):
        self.request = request
        self.model = model
        self.collection_ui = collection_ui


class CollectionUI(object):

    modelui_class = ModelUI

    create_include_fields: list = []
    create_exclude_fields: list = [
        'id', 'uuid', 'creator', 'created', 'modified', 'state', 'deleted',
        'xattrs', 'blobs'
    ]

    default_view = 'listing'

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
        {'title': 'Actions', 'name': 'structure:buttons'},
    ]

    def __init__(self, request, collection):
        self.request = request
        self.collection = collection

    def get_structure_column(self, obj, request, column_type):
        column_type = column_type.replace('structure:', '')
        coldata = request.app.get_structure_column(
            model=obj, request=request, name=column_type)
        return coldata
