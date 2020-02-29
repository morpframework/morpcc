from ..application.path import get_collection as get_app_col
from ..entity.path import get_collection as get_entity_col


class RestrictedEntityContent(object):
    def __init__(self, context):
        self.data = context.data
        self.save = context.save
        self.as_json = lambda: context.as_json()

    def __guarded_setitem__(self, key, value):
        self.__setitem__(key, value)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


class RestrictedEntityContentCollection(object):
    def __init__(self, context):
        def search(query=None, offset=0, limit=None, order_by=None):
            objs = context.search(query, offset, limit, order_by)
            return [RestrictedEntityContent(obj) for obj in objs]

        def create(data, deserialize=True):
            obj = context.create(data, deserialize=deserialize)
            return RestrictedEntityContent(obj)

        self.search = search
        self.create = create


class RestrictedApplication(object):
    def __init__(self, application):

        restricted_entities = {}
        for entity in application.entities():
            restricted_entities[entity["name"]] = RestrictedEntityContentCollection(
                entity.content_collection()
            )

        self.entities = restricted_entities

    def __getitem__(self, key):
        return self.entities[key]


class RestrictedContext(object):
    def __init__(self, context, request):

        app_col = get_app_col(request)
        apps = app_col.search()

        restricted_apps = {}
        for app in apps:
            restricted_apps[app["name"]] = RestrictedApplication(app)

        self.apps = restricted_apps

    def __getitem__(self, key):
        return self.apps[key]


class RestrictedRequest(object):
    def __init__(self, request):

        self.GET = request.GET
        self.POST = request.POST
        self.body = request.body
        self.headers = request.headers
        self.method = request.method
        self.json = request.json
