

class TypeRegistry(object):

    def __init__(self):
        self.typeinfo_factories = {}

    def register_typeinfo_factory(self, name, info_factory):
        info_factory['name'] = name
        self.typeinfo_factories[name] = info_factory

    def get_typeinfo(self, name, request):
        return self.typeinfo_factories[name](request)

    def get_typeinfos(self, request):
        res = {}
        for k, f in self.typeinfo_factories.items():
            res[k] = f(request)
        return res
