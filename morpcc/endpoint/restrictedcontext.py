from ..application.path import get_collection as get_app_col
from ..entity.path import get_collection as get_entity_col
from ..entitycontent.path import content_collection_factory


class RestrictedEntityContent(object):
    def __init__(self, context):
        self.data = context.data

        def update(data, deserialize=True):
            return context.update(data, deserialize=deserialize)

        def delete():
            return context.delete()

        self.update = update
        self.delete = delete
        self.save = context.save
        self.as_json = lambda: context.as_json()

    def __guarded_setitem__(self, key, value):
        self.__setitem__(key, value)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()


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
    def __init__(self, application, allow_invalid=False):
        self._application = application
        restricted_entities = {}
        for entity in application.application_schema().entities():
            restricted_entities[entity["name"]] = RestrictedEntityContentCollection(
                content_collection_factory(entity, application, allow_invalid)
            )

        self.entities = restricted_entities

    def allow_invalid(self):
        # FIXME: too hackish
        return RestrictedApplication(self._application, allow_invalid=True)

    def __getitem__(self, key):
        return self.entities[key]

    def keys(self):
        return self.entities.keys()

    def values(self):
        return self.entities.values()


class RestrictedContext(object):
    def __init__(self, request):

        app_col = get_app_col(request)
        apps = app_col.search()

        restricted_apps = {}
        for app in apps:
            restricted_apps[app["name"]] = RestrictedApplication(app)

        self.apps = restricted_apps

    def __getitem__(self, key):
        return self.apps[key]

    def keys(self):
        return self.apps.keys()

    def values(self):
        return self.apps.values()


class RestrictedRequest(object):
    def __init__(self, request):

        self.GET = request.GET
        self.POST = request.POST
        self.body = request.body
        self.headers = request.headers
        self.method = request.method
        self.json = lambda: request.json
