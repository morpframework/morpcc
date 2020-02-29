import rulez


class EntityReferenceValidator(object):
    def __init__(self, entity, attribute):
        self.entity = entity
        self.attribute = attribute

    def __call__(self, request, schema, field, value, mode=None):
        resource = self.get_resource(request, value)
        if not resource:
            return "Invalid reference : {}".format(value)

    def get_resource(self, request, identifier):
        col = self.entity.content_collection()
        models = col.search(rulez.field[self.attribute] == identifier)
        if models:
            return models[0]
        return None
