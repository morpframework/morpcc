import rulez


class EntityReferenceValidator(object):
    def __init__(self, entity_uuid, attribute):
        self.entity_uuid = entity_uuid
        self.attribute = attribute

    def __call__(self, request, schema, field, value, mode=None):
        resource = self.get_resource(request, value)
        if not resource:
            return "Invalid reference : {}".format(value)

    def get_resource(self, request, identifier):
        from ..entity.path import get_model as get_entity

        entity = get_entity(request, self.entity_uuid)
        col = entity.content_collection()
        models = col.search(rulez.field[self.attribute] == identifier)
        if models:
            return models[0]
        return None
